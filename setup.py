#!/usr/bin/env python3
"""
Setup script for Genshin Impact TCG Bot
This script helps users set up the bot environment and configuration.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header():
    """Print setup header"""
    print("=" * 60)
    print("🎴 Genshin Impact TCG Bot Setup 🎴")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    print("\n⚙️ Setting up environment configuration...")
    
    env_example_path = Path(".env.example")
    env_path = Path(".env")
    
    if not env_example_path.exists():
        print("❌ .env.example file not found")
        return False
    
    if env_path.exists():
        overwrite = input("📝 .env file already exists. Overwrite? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("⏭️ Skipping .env file creation")
            return True
    
    # Copy template
    with open(env_example_path, 'r') as f:
        env_content = f.read()
    
    print("\n🔧 Please provide the following configuration:")
    
    # Get Telegram Bot Token
    bot_token = input("🤖 Telegram Bot Token (from @BotFather): ").strip()
    if bot_token:
        env_content = env_content.replace("your_bot_token_here", bot_token)
    
    # Get Firebase configuration
    print("\n🔥 Firebase Configuration:")
    print("   (Get these from Firebase Console > Project Settings > Service Accounts)")
    
    firebase_project_id = input("   Project ID: ").strip()
    if firebase_project_id:
        env_content = env_content.replace("your_firebase_project_id", firebase_project_id)
    
    firebase_private_key_id = input("   Private Key ID: ").strip()
    if firebase_private_key_id:
        env_content = env_content.replace("your_private_key_id", firebase_private_key_id)
    
    firebase_private_key = input("   Private Key (with \\n): ").strip()
    if firebase_private_key:
        env_content = env_content.replace("your_private_key", firebase_private_key)
    
    firebase_client_email = input("   Client Email: ").strip()
    if firebase_client_email:
        env_content = env_content.replace("your_client_email", firebase_client_email)
    
    firebase_client_id = input("   Client ID: ").strip()
    if firebase_client_id:
        env_content = env_content.replace("your_client_id", firebase_client_id)
    
    # Write .env file
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully")
    return True

def create_data_directory():
    """Create data directory for exports and logs"""
    print("\n📁 Creating data directory...")
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print("✅ Data directory created")

def test_configuration():
    """Test if configuration is valid"""
    print("\n🧪 Testing configuration...")
    
    try:
        # Try to import and check basic configuration
        from config.settings import TELEGRAM_BOT_TOKEN, FIREBASE_CONFIG
        
        if not TELEGRAM_BOT_TOKEN:
            print("❌ Telegram Bot Token not configured")
            return False
        
        if not FIREBASE_CONFIG.get('project_id'):
            print("❌ Firebase configuration incomplete")
            return False
        
        print("✅ Configuration appears valid")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("1. Make sure your Firebase project has Firestore enabled")
    print("2. Set up your Telegram bot commands (optional):")
    print("   - Message @BotFather")
    print("   - Use /setcommands")
    print("   - Copy commands from README.md")
    print()
    print("🚀 To start the bot:")
    print("   python main.py")
    print()
    print("📚 For more information, see README.md")
    print()

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create environment file
    if not create_env_file():
        print("\n❌ Setup failed during environment configuration")
        sys.exit(1)
    
    # Create data directory
    create_data_directory()
    
    # Test configuration
    if not test_configuration():
        print("\n⚠️ Configuration test failed - please check your .env file")
        print("   You can still try running the bot, but it may not work properly")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)
