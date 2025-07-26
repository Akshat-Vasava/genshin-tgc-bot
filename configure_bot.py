#!/usr/bin/env python3
"""
Configuration script to set up the bot with Firebase credentials and bot token
"""

import os
import json

def setup_environment():
    """Set up environment variables for the bot"""
    
    # Firebase credentials from the JSON file
    firebase_config = {
        "project_id": "genshin-impact-tgc-bot",
        "private_key_id": "55dfcaee51e8f45427ca354f0670d3bf27bfdb99",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDkIZDJUsA3aHQ2\nul3LEPp1/0VPMdTe21Xtbu0LTrsrfB6l6SK50SdzSwoqYCA5ljUiOD94b0RoBPVi\nAe2x4tGJ4BBAe6KhtjdbrHt0etQOfUActtvyCUIhcZhWC7K9/0NoMJuv17v5Ay+i\nW3SyFSZ/Ohr66niZDEEcY3p7raFrvgRjzmMZEyjJ9jP8v/INo9Do8fWDOfYweiid\nt/3R5jI+xy25VaGJn7Qc1XJezZJEHyWV/QIaLWt8L5AsKtVNjd6f28syfGVX0rFY\nP+T5Wr/8Yhp5krz3VRrml+g3DhRwd486xQH9vXugigiv8R4bsyGfPKcT90cpc2vG\n3+BnPgAjAgMBAAECggEABw+k6B5YFb71beY51fm6DuHuVsOvl5BJahZ3XtS6hV+L\noU4EhaTcKDzn3STpim7ESUFdcZBcGS4iHDz8Cvf+zVoylpRdFc1KjFtb3OCaZLJq\nxBjC2QyBUACwmuU0zJ20i+qJPxmZ11zKYiebhpGSBfkZ8a9FOVOARm0r0t0udGO3\nzz4MpBThVfm6nbt9Ss7hGATBvtSuJMaho293DuAHmQEh/IERtMCxqaVbESIy6eb0\n8+b5Y0l6Cx0+3vbduGW2852pvJnNQufnVWZAFqDdzYxzGa02f1iMQ50qwAgSs7Aj\nmOSpn3lKkWErI/FAIkpHQFBoidx/YYrii+7Q36heeQKBgQD3SeKQ87WyrzfBnkgG\ngCh79v5CpAlw8eJTcR2hyWSxGLT23nV8iG1yqKdD5lyLUaZLajwVGXeq6UKwZiZB\ntMI1sd/E4IrmJUB2o+WqaZMN4IHMCVfjtLMrKQYPASigzqB05O3p2wGXv+DlBDon\nX3cjPlP0TXZ2XtUDIic9rDnVmwKBgQDsKunA1v2/ciFglFfcn5HvLSjL2UR2rHrh\nWCEkxu7ck9ZlV87kOP1zcysgNgaiGWvvU9T0irqBlnxN26GsnVjV4Piixt1CR2/P\nJHjVjXN2/oCgdBpERZezRP4liZcdNtdh4zdiUzTJOjvoyKDulxQ8JIBZI2IODqvG\nXwMeeXysGQKBgHtNhgFM496S67RJXhSPtqAJSkKkVGjS001T67iOGP0NGr61sdNE\nm34+hhifNqnpLogQEqFar4azBKO8a3r7zJLFfJRIejnDfV8q3guY1NBoj4/TYNWT\ndnsg23qD02RLY0qmE9M1dpfZ/yNydiTHvzn9jBMWxOjE5GXJk9N2mufdAoGBAOW5\ndHmtZ1TDau4sPi8QVP8nmWh45lzduAXdGRhSHeUYNVOND2X2favAmnGRu/AP9Grv\ny9U34OXPAQknHGPxBom9dX25HV6saHlBC/0GxAs60tnBNg+09jReZy0SYpj7UJUa\nVTRipZUb/UyZY9nRwdAi3WpXvbjY0oR6xWjuWbR5AoGBANi4cdDcywiVdJ/zU0vm\nhSa1g/x6ShLGSMIqHRHVc1BdOWpNrB79N3uuumg64beeCvUFMIhjJNiTwJpMXBLi\n2lqj/gqpU5xdkBb23rJAVa/WAHir1aUNNTe5ivWZBrwIDezOGyYPwB4GrYYJrE7m\n0nrhpmGoEiS0B5nawW0oBkqt\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-fbsvc@genshin-impact-tgc-bot.iam.gserviceaccount.com",
        "client_id": "112104983781220022843"
    }
    
    # Set environment variables
    os.environ['FIREBASE_PROJECT_ID'] = firebase_config['project_id']
    os.environ['FIREBASE_PRIVATE_KEY_ID'] = firebase_config['private_key_id']
    os.environ['FIREBASE_PRIVATE_KEY'] = firebase_config['private_key']
    os.environ['FIREBASE_CLIENT_EMAIL'] = firebase_config['client_email']
    os.environ['FIREBASE_CLIENT_ID'] = firebase_config['client_id']
    os.environ['FIREBASE_AUTH_URI'] = 'https://accounts.google.com/o/oauth2/auth'
    os.environ['FIREBASE_TOKEN_URI'] = 'https://oauth2.googleapis.com/token'
    
    # Bot configuration
    os.environ['BOT_NAME'] = 'Genshin TCG Bot'
    os.environ['DEBUG'] = 'True'
    
    print("✅ Firebase credentials configured!")
    
    # Ask for bot token
    bot_token = input("🤖 Please enter your Telegram bot token: ").strip()
    if bot_token:
        os.environ['TELEGRAM_BOT_TOKEN'] = bot_token
        print("✅ Bot token configured!")
        return True
    else:
        print("❌ Bot token is required!")
        return False

if __name__ == "__main__":
    if setup_environment():
        print("\n🚀 Starting the bot...")
        # Import and run the bot
        try:
            from main import main
            import asyncio
            asyncio.run(main())
        except Exception as e:
            print(f"❌ Error starting bot: {e}")
            print("\nPlease make sure you have:")
            print("1. Valid Telegram bot token from @BotFather")
            print("2. All dependencies installed")
