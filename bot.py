import os
import logging
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Language texts
TEXTS = {
    'en': {
        'welcome': 'Please select your language:',
        'camera_prompt': 'Welcome! Click the button below to open the camera and analyze food calories:',
        'help': 'Use the camera button to take a photo of your food!'
    },
    'ru': {
        'welcome': 'Пожалуйста, выберите язык:',
        'camera_prompt': 'Добро пожаловать! Нажмите кнопку ниже, чтобы открыть камеру и проанализировать калории в еде:',
        'help': 'Используйте кнопку камеры, чтобы сфотографировать еду!'
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with language selection buttons."""
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧", callback_data="lang_en"),
            InlineKeyboardButton("🇷🇺", callback_data="lang_ru")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Please select your language / Пожалуйста, выберите язык:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("lang_"):
        language = query.data.split("_")[1]
        context.user_data['language'] = language
        
        # Create button with web app
        web_app = WebAppInfo(url="https://ferter.onrender.com")
        keyboard = [[KeyboardButton("📸 Open Camera", web_app=web_app)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await query.message.reply_text(
            TEXTS[language]['camera_prompt'],
            reply_markup=reply_markup
        )
        # Delete the language selection message
        await query.message.delete()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    language = context.user_data.get('language', 'en')
    await update.message.reply_text(TEXTS[language]['help'])

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main() 