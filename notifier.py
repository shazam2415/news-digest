import os
import requests

def send_telegram_message(message):
    """Send message to Telegram bot"""
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        raise ValueError("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not found")
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Telegram has a 4096 character limit, so split if needed
    max_length = 4096
    
    if len(message) > max_length:
        print(f"⚠️ Message too long ({len(message)} chars), splitting into multiple messages...")
        # Split into chunks
        messages = [message[i:i+max_length] for i in range(0, len(message), max_length)]
    else:
        messages = [message]
    
    try:
        for msg in messages:
            payload = {
                'chat_id': chat_id,
                'text': msg,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            print(f"Telegram Response: {response.status_code}")
            print(f"Response Text: {response.text}")
            response.raise_for_status()
        
        return True
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to send Telegram message: {str(e)}")
