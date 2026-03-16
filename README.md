cat > README.md << 'EOF'
# 📰 News Digest - World Events Analyzer

Automated system that fetches world news every morning, summarizes it using AI, and sends it to your Telegram bot.

## Features

✅ Fetches top news daily from NewsAPI  
✅ Summarizes articles using Hugging Face AI  
✅ Sends digest to Telegram automatically  
✅ Runs on GitHub Actions (free)  
✅ Zero hosting costs  

## Setup

### 1. Get Your API Keys

- **NewsAPI Key**: https://newsapi.org/ (free, 100 requests/day)
- **Telegram Bot Token**: Create bot via [@BotFather](https://t.me/botfather) on Telegram
- **Telegram Chat ID**: Message your bot, then get ID from `https://api.telegram.org/botYOUR_TOKEN/getUpdates`

### 2. Create `.env` File

Create a `.env` file in the root directory with your keys.

### 3. Add GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions

Add these secrets:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `NEWSAPI_KEY`

### 4. Install Dependencies

```bash
pip install -r requirements.txt