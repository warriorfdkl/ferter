# Food Calorie Estimation Telegram Bot

This is a Telegram bot with a mini app that helps users estimate calories in food by taking photos.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your credentials:
```
BOT_TOKEN=your_telegram_bot_token
```

4. Run the bot:
```bash
python bot.py
```

## Features

- Telegram Mini App with camera integration
- Food photo analysis
- Calorie estimation
- Easy to use interface

## Deployment

The application is configured for deployment on Render.com. 