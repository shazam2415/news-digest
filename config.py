import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# NewsAPI Configuration
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')

# Summarization Configuration
SUMMARIZER_MODEL = "facebook/bart-large-cnn"
MAX_SUMMARY_LENGTH = 100
MIN_SUMMARY_LENGTH = 30

# Validate required variables
def validate_config():
    """Ensure all required environment variables are set"""
    required = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID', 'NEWSAPI_KEY']
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")
