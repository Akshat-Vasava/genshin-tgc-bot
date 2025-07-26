import logging
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, InlineQueryHandler
from config.settings import TELEGRAM_BOT_TOKEN, DEBUG
from config.firebase_config import firebase_manager
from bot.handlers.start import start_command, help_command, stats_command, button_callback
from bot.handlers.search import search_command, inline_query_handler, card_callback_handler
from bot.handlers.deck_builder import deck_command
from bot.handlers.rules import rules_command, rules_callback_handler
from scraper.data_processor import data_processor
import sys
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if not DEBUG else logging.DEBUG,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class GenshinTCGBot:
    """Main bot class"""
    
    def __init__(self):
        self.application = None
        self.initialized = False
    
    async def initialize(self):
        """Initialize the bot and its dependencies"""
        try:
            logger.info("Initializing Genshin TCG Bot...")
            
            # Check bot token
            if not TELEGRAM_BOT_TOKEN:
                logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
                return False
            
            # Initialize Firebase
            logger.info("Initializing Firebase...")
            if not firebase_manager.initialize():
                logger.error("Failed to initialize Firebase!")
                return False
            
            # Create application
            logger.info("Creating Telegram application...")
            self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
            
            # Register handlers
            self.register_handlers()
            
            # Initialize sample data if database is empty
            await self.initialize_sample_data()
            
            self.initialized = True
            logger.info("Bot initialization completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error during bot initialization: {e}")
            return False
    
    def register_handlers(self):
        """Register all bot command and callback handlers"""
        try:
            logger.info("Registering bot handlers...")
            
            # Command handlers
            self.application.add_handler(CommandHandler("start", start_command))
            self.application.add_handler(CommandHandler("help", help_command))
            self.application.add_handler(CommandHandler("search", search_command))
            self.application.add_handler(CommandHandler("deck", deck_command))
            self.application.add_handler(CommandHandler("rules", rules_command))
            self.application.add_handler(CommandHandler("stats", stats_command))
            
            # Callback query handlers
            self.application.add_handler(CallbackQueryHandler(button_callback, pattern="^action_"))
            self.application.add_handler(CallbackQueryHandler(card_callback_handler, pattern="^(show_card_|add_to_deck_|card_stats_)"))
            self.application.add_handler(CallbackQueryHandler(self.handle_deck_callbacks, pattern="^deck_"))
            self.application.add_handler(CallbackQueryHandler(rules_callback_handler, pattern="^rules_"))
            self.application.add_handler(CallbackQueryHandler(self.handle_admin_callbacks, pattern="^admin_"))
            
            # Inline query handler
            self.application.add_handler(InlineQueryHandler(inline_query_handler))
            
            # Message handlers
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
            
            # Error handler
            self.application.add_error_handler(self.error_handler)
            
            logger.info("All handlers registered successfully!")
            
        except Exception as e:
            logger.error(f"Error registering handlers: {e}")
            raise
    
    async def initialize_sample_data(self):
        """Initialize sample data if database is empty"""
        try:
            logger.info("Checking if sample data initialization is needed...")
            
            # Check if we have any cards in the database
            stats = data_processor.get_processing_stats()
            
            if stats['total_cards'] == 0:
                logger.info("Database is empty, loading sample cards...")
                result = data_processor.load_sample_cards()
                
                if result['success']:
                    logger.info(f"Successfully loaded {result['cards_saved']} sample cards")
                else:
                    logger.warning(f"Failed to load sample cards: {result['errors']}")
            else:
                logger.info(f"Database already contains {stats['total_cards']} cards")
                
        except Exception as e:
            logger.error(f"Error initializing sample data: {e}")
    
    async def handle_deck_callbacks(self, update, context):
        """Handle deck-related callback queries"""
        try:
            query = update.callback_query
            await query.answer()
            
            callback_data = query.data
            user_id = str(query.from_user.id)
            
            if callback_data.startswith("deck_show_"):
                deck_id = callback_data.replace("deck_show_", "")
                from bot.utils.database import db_manager
                deck = db_manager.get_deck(deck_id)
                
                if deck and deck.user_id == user_id:
                    from bot.handlers.deck_builder import handle_deck_show
                    # Create a mock update object for the handler
                    class MockUpdate:
                        def __init__(self, message):
                            self.message = message
                    
                    mock_update = MockUpdate(query.message)
                    await handle_deck_show(mock_update, user_id, deck.name)
                else:
                    await query.edit_message_text("❌ Deck not found or access denied.")
            
            elif callback_data.startswith("deck_delete_confirmed_"):
                deck_id = callback_data.replace("deck_delete_confirmed_", "")
                from bot.utils.database import db_manager
                
                if db_manager.delete_deck(deck_id, user_id):
                    await query.edit_message_text(
                        "✅ **Deck deleted successfully!**\n\n"
                        "Use `/deck list` to see your remaining decks.",
                        parse_mode='Markdown'
                    )
                else:
                    await query.edit_message_text("❌ Failed to delete deck.")
            
            elif callback_data.startswith("add_card_to_deck_"):
                parts = callback_data.replace("add_card_to_deck_", "").split("_")
                if len(parts) >= 2:
                    deck_id = parts[0]
                    card_id = "_".join(parts[1:])
                    
                    from bot.utils.database import db_manager
                    deck = db_manager.get_deck(deck_id)
                    card = db_manager.get_card(card_id)
                    
                    if deck and card and deck.user_id == user_id:
                        from bot.handlers.deck_builder import add_card_to_deck
                        class MockUpdate:
                            def __init__(self, message):
                                self.message = message
                        
                        mock_update = MockUpdate(query.message)
                        await add_card_to_deck(mock_update, deck, card, 1)
                    else:
                        await query.edit_message_text("❌ Deck or card not found.")
                        
        except Exception as e:
            logger.error(f"Error handling deck callback: {e}")
            await query.edit_message_text("❌ An error occurred.")
    
    async def handle_admin_callbacks(self, update, context):
        """Handle admin-related callback queries"""
        try:
            query = update.callback_query
            await query.answer()
            
            callback_data = query.data
            user_id = str(query.from_user.id)
            
            # Simple admin check (in production, use proper admin system)
            if callback_data == "admin_scrape_cards":
                await query.edit_message_text(
                    "🔄 **Starting card scraping process...**\n\n"
                    "This may take several minutes. Please wait...",
                    parse_mode='Markdown'
                )
                
                # Run scraping in background
                result = data_processor.scrape_and_process_all_cards()
                
                if result['success']:
                    await query.edit_message_text(
                        f"✅ **Card scraping completed!**\n\n"
                        f"📊 **Results:**\n"
                        f"• Cards processed: {result['cards_processed']}\n"
                        f"• Cards saved: {result['cards_saved']}\n"
                        f"• Errors: {len(result['errors'])}\n\n"
                        f"Use `/search` to test the new cards!",
                        parse_mode='Markdown'
                    )
                else:
                    error_summary = "\n".join(result['errors'][:3])
                    await query.edit_message_text(
                        f"❌ **Card scraping failed!**\n\n"
                        f"**Errors:**\n{error_summary}\n\n"
                        f"Check logs for more details.",
                        parse_mode='Markdown'
                    )
            
            elif callback_data == "admin_load_samples":
                result = data_processor.load_sample_cards()
                
                if result['success']:
                    await query.edit_message_text(
                        f"✅ **Sample cards loaded!**\n\n"
                        f"Loaded {result['cards_saved']} sample cards.",
                        parse_mode='Markdown'
                    )
                else:
                    await query.edit_message_text(
                        "❌ **Failed to load sample cards!**",
                        parse_mode='Markdown'
                    )
                        
        except Exception as e:
            logger.error(f"Error handling admin callback: {e}")
            await query.edit_message_text("❌ An error occurred.")
    
    async def handle_text_message(self, update, context):
        """Handle regular text messages"""
        try:
            user_id = str(update.effective_user.id)
            message_text = update.message.text.lower().strip()
            
            # Update user activity
            from bot.utils.database import db_manager
            db_manager.update_user_activity(user_id)
            
            # Handle common queries
            if any(keyword in message_text for keyword in ['help', 'commands', 'what can you do']):
                await help_command(update, context)
            elif any(keyword in message_text for keyword in ['search', 'find', 'card']):
                await update.message.reply_text(
                    "🔍 To search for cards, use:\n"
                    "`/search <card name>`\n\n"
                    "Example: `/search Diluc`",
                    parse_mode='Markdown'
                )
            elif any(keyword in message_text for keyword in ['deck', 'build']):
                await update.message.reply_text(
                    "🃏 To manage decks, use:\n"
                    "`/deck list` - View your decks\n"
                    "`/deck create \"Deck Name\"` - Create new deck\n\n"
                    "Use `/help` for more deck commands!",
                    parse_mode='Markdown'
                )
            else:
                # Generic response
                await update.message.reply_text(
                    "👋 Hi! I'm the Genshin Impact TCG Bot.\n\n"
                    "Use `/help` to see what I can do, or try:\n"
                    "• `/search <card name>` - Find cards\n"
                    "• `/deck list` - Manage decks\n"
                    "• `/start` - Main menu",
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logger.error(f"Error handling text message: {e}")
            await update.message.reply_text(
                "❌ Sorry, something went wrong. Please try again or use `/help`.",
                parse_mode='Markdown'
            )
    
    async def error_handler(self, update, context):
        """Handle errors"""
        try:
            logger.error(f"Update {update} caused error {context.error}")
            
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "❌ An unexpected error occurred. The developers have been notified.\n\n"
                    "Please try again or use `/help` for assistance.",
                    parse_mode='Markdown'
                )
        except Exception as e:
            logger.error(f"Error in error handler: {e}")
    
    async def run(self):
        """Run the bot"""
        if not self.initialized:
            logger.error("Bot not initialized! Call initialize() first.")
            return
        
        try:
            logger.info("Starting Genshin TCG Bot...")
            
            # Start the bot
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            
            logger.info("Bot is now running! Press Ctrl+C to stop.")
            
            # Keep the bot running
            import signal
            import asyncio
            
            # Set up signal handlers for graceful shutdown
            stop_signals = (signal.SIGTERM, signal.SIGINT)
            for sig in stop_signals:
                signal.signal(sig, lambda s, f: asyncio.create_task(self.application.stop()))
            
            # Keep running until interrupted
            try:
                await asyncio.Event().wait()
            except asyncio.CancelledError:
                pass
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Error running bot: {e}")
        finally:
            # Cleanup
            if self.application:
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()
            logger.info("Bot shutdown completed")

async def main():
    """Main function"""
    try:
        # Create and initialize bot
        bot = GenshinTCGBot()
        
        if await bot.initialize():
            await bot.run()
        else:
            logger.error("Failed to initialize bot")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    # Run the bot
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
