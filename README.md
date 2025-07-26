# Genshin Impact TCG Bot 🎴

A comprehensive Telegram bot for Genshin Impact's Genius Invokation TCG (Trading Card Game). This bot helps players search for cards, build decks, validate deck compositions, and learn game rules.

## Features ✨

### 🔍 Card Search
- Search cards by name, type, or element
- Fuzzy search for partial matches
- Detailed card information display
- Inline query support for quick searches

### 🃏 Deck Builder
- Create and manage multiple decks
- Add/remove cards with validation
- Deck rule validation (30 cards, 3 characters, etc.)
- Share decks with other players

### 📊 Deck Validation
- Real-time deck validation against TCG rules
- Helpful suggestions and warnings
- Tournament-ready deck verification

### 📚 Game Rules & Guides
- Quick reference for game mechanics
- Elemental reaction guides
- Deck building tips

### 📈 User Statistics
- Track your bot usage
- Deck creation statistics
- Search history

## Installation & Setup 🚀

### Prerequisites
- Python 3.8 or higher
- Firebase project
- Telegram Bot Token

### 1. Clone the Repository
```bash
git clone <repository-url>
cd genshin-tcg-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
1. Copy `.env.example` to `.env`
2. Fill in your configuration:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Firebase Configuration
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
FIREBASE_CLIENT_ID=your_client_id

# Bot Configuration
BOT_NAME=Genshin TCG Bot
DEBUG=False
```

### 4. Firebase Setup
1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Firestore Database
3. Create a service account and download the credentials
4. Extract the credentials and add them to your `.env` file

### 5. Telegram Bot Setup
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Get your bot token and add it to `.env`
4. Set bot commands (optional):
```
start - Start the bot and get welcome message
help - Show available commands
search - Search for cards by name
deck - Deck management commands
rules - Show TCG rules and guides
stats - Show your bot usage statistics
```

### 6. Run the Bot
```bash
python main.py
```

## Usage Guide 📖

### Basic Commands

#### `/start`
- Welcome message and main menu
- Interactive buttons for quick access

#### `/search <card_name>`
- Search for cards by name or keyword
- Examples:
  - `/search Diluc` - Find Diluc character card
  - `/search Pyro` - Find Pyro-related cards
  - `/search weapon` - Find weapon cards

#### `/deck <action>`
Available deck actions:
- `/deck list` - Show all your decks
- `/deck create "Deck Name"` - Create a new deck
- `/deck show "Deck Name"` - View deck details
- `/deck add "Deck Name" "Card Name"` - Add card to deck
- `/deck remove "Deck Name" "Card Name"` - Remove card from deck
- `/deck delete "Deck Name"` - Delete a deck

#### `/stats`
- View your usage statistics
- Deck counts and favorite card types

#### `/help`
- Comprehensive help and command examples

### Inline Queries
Use `@your_bot_name card_name` in any chat for quick card searches.

## Project Structure 📁

```
genshin-tcg-bot/
├── main.py                 # Bot entry point
├── config/
│   ├── settings.py         # Configuration settings
│   └── firebase_config.py  # Firebase setup
├── bot/
│   ├── handlers/
│   │   ├── start.py        # Start command handler
│   │   ├── search.py       # Card search functionality
│   │   └── deck_builder.py # Deck building features
│   └── utils/
│       ├── database.py     # Firebase operations
│       └── validators.py   # Input validation
├── models/
│   ├── card.py            # Card data models
│   └── deck.py            # Deck data models
├── scraper/
│   ├── wiki_scraper.py    # Web scraping for card data
│   └── data_processor.py  # Data processing and management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Card Data Management 📋

### Sample Data
The bot includes sample cards for testing. When first run, it will automatically load sample cards if the database is empty.

### Web Scraping
The bot includes a web scraper for the Genshin Impact Fandom Wiki:
```python
from scraper.data_processor import data_processor

# Scrape and process all cards
result = data_processor.scrape_and_process_all_cards()

# Load sample cards for testing
result = data_processor.load_sample_cards()
```

### Manual Data Import
You can import card data from JSON files:
```python
result = data_processor.import_cards_from_json('path/to/cards.json')
```

## Database Schema 🗄️

### Collections

#### `cards`
- Card information (characters, actions, equipment, etc.)
- Searchable by name, type, element

#### `users`
- User profiles and statistics
- Activity tracking

#### `decks`
- User-created decks
- Card lists and metadata

## Development 🛠️

### Adding New Features
1. Create handlers in `bot/handlers/`
2. Add models in `models/` if needed
3. Register handlers in `main.py`
4. Update help text and documentation

### Testing
```bash
# Run with debug mode
DEBUG=True python main.py
```

### Logging
Logs are written to `bot.log` and console output.

## Deployment 🚀

### Heroku
1. Create a Heroku app
2. Set environment variables in Heroku dashboard
3. Deploy using Git or GitHub integration

### Railway
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

### VPS/Server
1. Set up Python environment
2. Configure environment variables
3. Use process manager like PM2 or systemd
4. Set up reverse proxy if needed

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting 🔧

### Common Issues

#### Bot doesn't respond
- Check if bot token is correct
- Verify Firebase configuration
- Check logs for error messages

#### Card search returns no results
- Ensure card data is loaded
- Check database connection
- Try loading sample cards

#### Deck operations fail
- Verify user permissions
- Check deck validation rules
- Ensure Firebase write permissions

### Debug Mode
Enable debug mode in `.env`:
```env
DEBUG=True
```

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- Genshin Impact and Genius Invokation TCG by miHoYo/HoYoverse
- Genshin Impact Fandom Wiki for card information
- Python Telegram Bot library
- Firebase for database services

## Support 💬

For support, questions, or feature requests:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Create an issue on GitHub
4. Contact the development team

---

**Disclaimer**: This bot is not officially affiliated with miHoYo/HoYoverse. Genshin Impact and all related content are trademarks of miHoYo/HoYoverse.
