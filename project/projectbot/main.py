import asyncio
import logging
import sys
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN, DEBUG_MODE
from bot_instance import bot

from handlers.start import register_start_handlers
from handlers.daily_test import register_daily_test_handlers
from handlers.ideas import register_idea_handlers
from database import init_db

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create dispatcher
dp = Dispatcher()

async def main():
    """Main bot function with comprehensive error handling and logging"""
    try:
        logger.info("=" * 50)
        logger.info("Starting Telegram Bot...")
        logger.info(f"Bot token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-4:]}")
        logger.info(f"Debug mode: {DEBUG_MODE}")
        
        # Initialize database first
        logger.info("Initializing database...")
        await init_db()
        
        # Register all handlers
        logger.info("Registering handlers...")
        register_start_handlers(dp)
        register_daily_test_handlers(dp)
        register_idea_handlers(dp)
        
        logger.info("All handlers registered successfully")
        logger.info("Bot is ready to start polling...")
        logger.info("=" * 50)
        
        # Start polling with proper configuration
        await dp.start_polling(
            bot,
            handle_signals=False,
            allowed_updates=dp.resolve_used_update_types()
        )
        
    except Exception as e:
        logger.error(f"Fatal error in main function: {e}")
        logger.exception("Full traceback:")
        raise

if __name__ == "__main__":
    try:
        logger.info("Bot startup initiated")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        logger.exception("Full traceback:")
        raise