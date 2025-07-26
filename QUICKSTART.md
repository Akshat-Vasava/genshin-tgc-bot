# Quick Start Guide 🚀

Get your Genshin Impact TCG Bot up and running in minutes!

## Prerequisites ✅

- Python 3.8 or higher
- A Telegram account
- A Google account (for Firebase)

## Step 1: Get Your Bot Token 🤖

1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Choose a name and username for your bot
4. Copy the bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Step 2: Set Up Firebase 🔥

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter a project name (e.g., "genshin-tcg-bot")
4. Disable Google Analytics (not needed)
5. Click "Create project"

### Enable Firestore Database

1. In your Firebase project, click "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode"
4. Select a location close to you
5. Click "Done"

### Get Service Account Credentials

1. Go to Project Settings (gear icon) > Service accounts
2. Click "Generate new private key"
3. Download the JSON file
4. Keep this file safe - you'll need the values from it

## Step 3: Clone and Setup 📥

```bash
# Clone the repository
git clone <repository-url>
cd genshin-tcg-bot

# Run the setup script
python setup.py
```

The setup script will:
- Check your Python version
- Install required packages
- Guide you through configuration
- Create the necessary files

## Step 4: Configure Your Bot ⚙️

When prompted by the setup script, provide:

1. **Telegram Bot Token**: The token from BotFather
2. **Firebase Configuration**: Values from your downloaded JSON file:
   - `project_id`
   - `private_key_id`
   - `private_key` (include the `\n` characters)
   - `client_email`
   - `client_id`

## Step 5: Run Your Bot 🎉

```bash
python main.py
```

You should see:
```
INFO - Initializing Genshin TCG Bot...
INFO - Bot is now running! Press Ctrl+C to stop.
```

## Step 6: Test Your Bot 🧪

1. Open Telegram
2. Search for your bot by username
3. Send `/start`
4. You should see the welcome message with interactive buttons!

## Common Issues 🔧

### "Bot token not found"
- Make sure you copied the token correctly to your `.env` file
- Check that there are no extra spaces

### "Failed to initialize Firebase"
- Verify your Firebase credentials in `.env`
- Make sure Firestore is enabled in your Firebase project
- Check that your private key includes `\n` characters

### "No cards found"
- The bot starts with sample cards automatically
- Try `/search Diluc` to test

### Import errors
- Make sure you ran `python setup.py` first
- Try `pip install -r requirements.txt` manually

## Next Steps 📈

Once your bot is running:

1. **Set Bot Commands** (optional):
   - Message @BotFather
   - Send `/setcommands`
   - Copy the commands from the main README.md

2. **Customize Your Bot**:
   - Edit the welcome message in `bot/handlers/start.py`
   - Add more sample cards in `scraper/data_processor.py`
   - Modify the bot name in `.env`

3. **Deploy Your Bot**:
   - See the main README.md for deployment options
   - Consider using Heroku, Railway, or a VPS

## Getting Help 💬

- Check the main README.md for detailed documentation
- Look at the logs in `bot.log` for error details
- Make sure all your configuration is correct

## Sample Commands to Try 🎮

```
/start          - Welcome message and main menu
/search Diluc   - Search for Diluc character card
/deck create "My First Deck"  - Create a new deck
/deck list      - View your decks
/rules basic    - Learn basic game rules
/stats          - View your bot usage statistics
```

---

**🎉 Congratulations!** Your Genshin Impact TCG Bot is now ready to help players build decks and learn the game!
