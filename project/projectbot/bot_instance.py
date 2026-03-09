# bot_instance.py
from aiogram import Bot
from config import BOT_TOKEN

# Create bot instance with error handling
try:
    bot = Bot(token=BOT_TOKEN)
except Exception as e:
    print(f"Failed to create bot instance: {e}")
    raise
