#!/usr/bin/env python3
"""
Comprehensive test script for Genshin Impact TCG Bot
Tests all components without requiring actual Telegram/Firebase connections
"""

import sys
import os
import traceback
from datetime import datetime

def print_test_header(test_name):
    """Print test section header"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {test_name}")
    print(f"{'='*60}")

def print_test_result(test_name, success, details=""):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"   {details}")

def test_imports():
    """Test all module imports"""
    print_test_header("Module Imports")
    
    tests = []
    
    # Test core Python modules
    try:
        import logging
        import asyncio
        import json
        import os
        import time
        import re
        from datetime import datetime
        from typing import List, Dict, Any, Optional
        from dataclasses import dataclass, asdict
        tests.append(("Core Python modules", True))
    except Exception as e:
        tests.append(("Core Python modules", False, str(e)))
    
    # Test external packages
    external_packages = [
        ("python-telegram-bot", "telegram"),
        ("firebase-admin", "firebase_admin"),
        ("requests", "requests"),
        ("beautifulsoup4", "bs4"),
        ("python-dotenv", "dotenv"),
        ("fuzzywuzzy", "fuzzywuzzy"),
        ("Pillow", "PIL")
    ]
    
    for package_name, import_name in external_packages:
        try:
            __import__(import_name)
            tests.append((f"{package_name} package", True))
        except ImportError as e:
            tests.append((f"{package_name} package", False, f"Missing: {package_name}"))
    
    # Test project modules
    project_modules = [
        ("config.settings", "config/settings.py"),
        ("config.firebase_config", "config/firebase_config.py"),
        ("models.card", "models/card.py"),
        ("models.deck", "models/deck.py"),
        ("bot.utils.database", "bot/utils/database.py"),
        ("bot.utils.validators", "bot/utils/validators.py"),
        ("bot.handlers.start", "bot/handlers/start.py"),
        ("bot.handlers.search", "bot/handlers/search.py"),
        ("bot.handlers.deck_builder", "bot/handlers/deck_builder.py"),
        ("bot.handlers.rules", "bot/handlers/rules.py"),
        ("scraper.wiki_scraper", "scraper/wiki_scraper.py"),
        ("scraper.data_processor", "scraper/data_processor.py")
    ]
    
    for module_name, file_path in project_modules:
        try:
            __import__(module_name)
            tests.append((f"Project module: {module_name}", True))
        except Exception as e:
            tests.append((f"Project module: {module_name}", False, str(e)))
    
    # Print results
    for test_name, success, *details in tests:
        print_test_result(test_name, success, details[0] if details else "")
    
    return all(test[1] for test in tests)

def test_models():
    """Test data models"""
    print_test_header("Data Models")
    
    tests = []
    
    try:
        from models.card import Card, CharacterCard, ActionCard, EquipmentCard, SupportCard, EventCard, CardFactory
        from models.deck import Deck, DeckCard
        
        # Test Card creation
        try:
            card = Card(
                id="test_card",
                name="Test Card",
                card_type="ACTION",
                cost=2,
                description="A test card for validation"
            )
            tests.append(("Card model creation", True))
        except Exception as e:
            tests.append(("Card model creation", False, str(e)))
        
        # Test CharacterCard creation
        try:
            char_card = CharacterCard(
                id="test_char",
                name="Test Character",
                card_type="CHARACTER",
                cost=0,
                description="A test character",
                element="PYRO",
                weapon="SWORD",
                hp=10,
                max_energy=3,
                skills=[]
            )
            tests.append(("CharacterCard model creation", True))
        except Exception as e:
            tests.append(("CharacterCard model creation", False, str(e)))
        
        # Test Deck creation
        try:
            deck = Deck(
                id="test_deck",
                name="Test Deck",
                user_id="123456",
                cards=[]
            )
            tests.append(("Deck model creation", True))
        except Exception as e:
            tests.append(("Deck model creation", False, str(e)))
        
        # Test CardFactory
        try:
            card_data = {
                'id': 'factory_test',
                'name': 'Factory Test Card',
                'card_type': 'ACTION',
                'cost': 1,
                'description': 'Test card from factory'
            }
            factory_card = CardFactory.create_card(card_data)
            tests.append(("CardFactory functionality", True))
        except Exception as e:
            tests.append(("CardFactory functionality", False, str(e)))
            
    except Exception as e:
        tests.append(("Model imports", False, str(e)))
    
    # Print results
    for test_name, success, *details in tests:
        print_test_result(test_name, success, details[0] if details else "")
    
    return all(test[1] for test in tests)

def test_validators():
    """Test validation functions"""
    print_test_header("Validators")
    
    tests = []
    
    try:
        from bot.utils.validators import DeckValidator, InputValidator, CommandValidator
        from models.deck import Deck
        
        # Test deck name validation
        try:
            result = DeckValidator.validate_deck_name("Valid Deck Name")
            tests.append(("Valid deck name validation", result['is_valid']))
            
            result = DeckValidator.validate_deck_name("")
            tests.append(("Empty deck name validation", not result['is_valid']))
        except Exception as e:
            tests.append(("Deck name validation", False, str(e)))
        
        # Test input sanitization
        try:
            sanitized = InputValidator.sanitize_input("  Test <script> Input  ")
            tests.append(("Input sanitization", "script" not in sanitized))
        except Exception as e:
            tests.append(("Input sanitization", False, str(e)))
        
        # Test search query validation
        try:
            result = InputValidator.validate_search_query("Diluc")
            tests.append(("Valid search query", result['is_valid']))
            
            result = InputValidator.validate_search_query("")
            tests.append(("Empty search query", not result['is_valid']))
        except Exception as e:
            tests.append(("Search query validation", False, str(e)))
        
        # Test command validation
        try:
            result = CommandValidator.validate_search_command(["Diluc"])
            tests.append(("Search command validation", result['is_valid']))
            
            result = CommandValidator.validate_deck_command(["create", "Test Deck"])
            tests.append(("Deck command validation", result['is_valid']))
        except Exception as e:
            tests.append(("Command validation", False, str(e)))
            
    except Exception as e:
        tests.append(("Validator imports", False, str(e)))
    
    # Print results
    for test_name, success, *details in tests:
        print_test_result(test_name, success, details[0] if details else "")
    
    return all(test[1] for test in tests)

def test_deck_operations():
    """Test deck operations without database"""
    print_test_header("Deck Operations")
    
    tests = []
    
    try:
        from models.deck import Deck, DeckCard
        from models.card import Card
        
        # Create test deck
        deck = Deck(
            id="test_deck",
            name="Test Deck",
            user_id="123456",
            cards=[]
        )
        
        # Test adding cards
        try:
            success = deck.add_card("card1", "Test Card 1", "CHARACTER", 1)
            tests.append(("Add card to deck", success))
            
            success = deck.add_card("card2", "Test Card 2", "ACTION", 2)
            tests.append(("Add multiple copies", success))
        except Exception as e:
            tests.append(("Add card to deck", False, str(e)))
        
        # Test deck validation
        try:
            validation = deck.validate_deck()
            tests.append(("Deck validation", isinstance(validation, dict)))
        except Exception as e:
            tests.append(("Deck validation", False, str(e)))
        
        # Test card counting
        try:
            total = deck.get_total_cards()
            char_count = deck.get_character_count()
            tests.append(("Card counting", total == 3 and char_count == 1))
        except Exception as e:
            tests.append(("Card counting", False, str(e)))
        
        # Test deck summary
        try:
            summary = deck.get_deck_summary()
            tests.append(("Deck summary generation", isinstance(summary, str) and len(summary) > 0))
        except Exception as e:
            tests.append(("Deck summary generation", False, str(e)))
            
    except Exception as e:
        tests.append(("Deck operation setup", False, str(e)))
    
    # Print results
    for test_name, success, *details in tests:
        print_test_result(test_name, success, details[0] if details else "")
    
    return all(test[1] for test in tests)

def test_scraper():
    """Test scraper components"""
    print_test_header("Web Scraper")
    
    tests = []
    
    try:
        from scraper.wiki_scraper import GenshinTCGWikiScraper
        from scraper.data_processor import TCGDataProcessor
        
        # Test scraper initialization
        try:
            scraper = GenshinTCGWikiScraper()
            tests.append(("Scraper initialization", True))
        except Exception as e:
            tests.append(("Scraper initialization", False, str(e)))
        
        # Test data processor initialization
        try:
            processor = TCGDataProcessor()
            tests.append(("Data processor initialization", True))
        except Exception as e:
            tests.append(("Data processor initialization", False, str(e)))
        
        # Test card ID generation
        try:
            scraper = GenshinTCGWikiScraper()
            card_id = scraper.generate_card_id("Test Card", "CHARACTER")
            tests.append(("Card ID generation", isinstance(card_id, str) and len(card_id) > 0))
        except Exception as e:
            tests.append(("Card ID generation", False, str(e)))
        
        # Test text cleaning
        try:
            processor = TCGDataProcessor()
            cleaned = processor.clean_text("  Test   text with   spaces  ")
            tests.append(("Text cleaning", cleaned == "Test text with spaces"))
        except Exception as e:
            tests.append(("Text cleaning", False, str(e)))
            
    except Exception as e:
        tests.append(("Scraper imports", False, str(e)))
    
    # Print results
    for test_name, success, *details in tests:
        print_test_result(test_name, success, details[0] if details else "")
    
    return all(test[1] for test in tests)

def test_configuration():
    """Test configuration loading"""
    print_test_header("Configuration")
    
    tests = []
    
    try:
        from config.settings import COMMANDS, DECK_RULES, CARD_TYPES, ELEMENTS
        
        # Test configuration constants
        tests.append(("COMMANDS configuration", isinstance(COMMANDS, dict) and len(COMMANDS) > 0))
        tests.append(("DECK_RULES configuration", isinstance(DECK_RULES, dict) and 'max_cards' in DECK_RULES))
        tests.append(("CARD_TYPES configuration", isinstance(CARD_TYPES, dict) and 'CHARACTER' in CARD_TYPES))
        tests.append(("ELEMENTS configuration", isinstance(ELEMENTS, dict) and 'PYRO' in ELEMENTS))
        
        # Test deck rules values
        tests.append(("Max cards rule", DECK_RULES.get('max_cards') == 30))
        tests.append(("Max characters rule", DECK_RULES.get('max_characters') == 3))
        tests.append(("Max copies rule", DECK_RULES.get('max_copies_per_card') == 2))
        
    except Exception as e:
        tests.append(("Configuration loading", False, str(e)))
    
    # Print results
    for test_name, success, *details in tests:
        print_test_result(test_name, success, details[0] if details else "")
    
    return all(test[1] for test in tests)

def test_handlers():
    """Test handler functions (without Telegram context)"""
    print_test_header("Bot Handlers")
    
    tests = []
    
    # Test handler imports
    try:
        from bot.handlers.start import start_command, help_command, stats_command
        from bot.handlers.search import search_command
        from bot.handlers.deck_builder import deck_command
        from bot.handlers.rules import rules_command
        tests.append(("Handler imports", True))
    except Exception as e:
        tests.append(("Handler imports", False, str(e)))
    
    # Test if handlers are callable
    try:
        from bot.handlers.start import start_command, help_command
        tests.append(("Start command callable", callable(start_command)))
        tests.append(("Help command callable", callable(help_command)))
    except Exception as e:
        tests.append(("Handler callability", False, str(e)))
    
    # Print results
    for test_name, success, *details in tests:
        print_test_result(test_name, success, details[0] if details else "")
    
    return all(test[1] for test in tests)

def test_main_bot():
    """Test main bot class"""
    print_test_header("Main Bot Class")
    
    tests = []
    
    try:
        from main import GenshinTCGBot
        
        # Test bot initialization
        try:
            bot = GenshinTCGBot()
            tests.append(("Bot class instantiation", True))
        except Exception as e:
            tests.append(("Bot class instantiation", False, str(e)))
        
        # Test bot methods exist
        try:
            bot = GenshinTCGBot()
            tests.append(("Initialize method exists", hasattr(bot, 'initialize')))
            tests.append(("Register handlers method exists", hasattr(bot, 'register_handlers')))
            tests.append(("Run method exists", hasattr(bot, 'run')))
        except Exception as e:
            tests.append(("Bot methods", False, str(e)))
            
    except Exception as e:
        tests.append(("Main bot import", False, str(e)))
    
    # Print results
    for test_name, success, *details in tests:
        print_test_result(test_name, success, details[0] if details else "")
    
    return all(test[1] for test in tests)

def test_file_structure():
    """Test project file structure"""
    print_test_header("File Structure")
    
    tests = []
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "QUICKSTART.md",
        "setup.py",
        ".env.example",
        "config/settings.py",
        "config/firebase_config.py",
        "models/card.py",
        "models/deck.py",
        "bot/handlers/start.py",
        "bot/handlers/search.py",
        "bot/handlers/deck_builder.py",
        "bot/handlers/rules.py",
        "bot/utils/database.py",
        "bot/utils/validators.py",
        "scraper/wiki_scraper.py",
        "scraper/data_processor.py"
    ]
    
    for file_path in required_files:
        exists = os.path.exists(file_path)
        tests.append((f"File exists: {file_path}", exists))
    
    # Print results
    for test_name, success, *details in tests:
        print_test_result(test_name, success, details[0] if details else "")
    
    return all(test[1] for test in tests)

def run_all_tests():
    """Run all tests and provide summary"""
    print("🎴 Genshin Impact TCG Bot - Comprehensive Testing")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_results = []
    
    # Run all test suites
    test_suites = [
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("Data Models", test_models),
        ("Validators", test_validators),
        ("Deck Operations", test_deck_operations),
        ("Web Scraper", test_scraper),
        ("Bot Handlers", test_handlers),
        ("Main Bot Class", test_main_bot)
    ]
    
    for suite_name, test_func in test_suites:
        try:
            result = test_func()
            test_results.append((suite_name, result))
        except Exception as e:
            print(f"\n❌ Test suite '{suite_name}' failed with error: {e}")
            traceback.print_exc()
            test_results.append((suite_name, False))
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for suite_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {suite_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All tests passed! The bot is ready for deployment.")
        return True
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
