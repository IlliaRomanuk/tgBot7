# main.py - COMPLETE REFACTOR: Production-ready Telegram bot
import asyncio
import logging
import sys
from aiogram import Dispatcher, Bot, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, DEBUG_MODE

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Enable aiogram debug logging
if DEBUG_MODE:
    logging.getLogger("aiogram").setLevel(logging.DEBUG)
    logging.getLogger("aiogram.dispatcher").setLevel(logging.DEBUG)
    logging.getLogger("aiogram.event").setLevel(logging.DEBUG)
    logger.info("✅ Aiogram debug logging enabled")

# Create bot and dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties())
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def main():
    """Main bot function - REFACTORED for production"""
    try:
        logger.info("=" * 60)
        logger.info("🚀 Starting Production Telegram Bot...")
        logger.info(f"🔑 Bot token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-4:]}")
        
        # Initialize database
        logger.info("📊 Initializing database...")
        from database import init_db
        await init_db()
        logger.info("✅ Database initialized successfully")
        
        # Setup scheduler
        logger.info("⏰ Setting up scheduler...")
        from scheduler import setup_scheduler
        scheduler = setup_scheduler(bot)
        scheduler.start()
        logger.info("✅ Scheduler started with bot instance")
        
        # Import handlers - CLEAN IMPORTS
        logger.info("📦 Importing handlers...")
        from handlers.start_handler import router as start_router
        from handlers.test_handler import router as test_router
        from handlers.idea_handler import router as idea_router
        from handlers.problem_handler import router as problem_router
        
        # Register routers in CORRECT ORDER
        logger.info("🔗 Registering routers in correct priority order...")
        
        # 1. Commands (highest priority)
        dp.include_router(start_router)
        logger.info("✅ Start router registered (/start, /help)")
        
        # 2. Button flows (medium priority)
        dp.include_router(test_router)
        logger.info("✅ Test router registered (пройти)")
        
        dp.include_router(idea_router)
        logger.info("✅ Idea router registered (иде)")
        
        dp.include_router(problem_router)
        logger.info("✅ Problem router registered (проблем)")
        
        # 3. Global debug handler (lowest priority) - ONLY for truly unhandled messages
        @dp.message()
        async def global_debug_handler(message: types.Message):
            """Global debug handler - Catches ONLY truly unhandled messages"""
            # Comprehensive diagnostic logging
            print(f"🔍 [GLOBAL DEBUG] Raw message: {repr(message.text)}")
            print(f"🔍 [GLOBAL DEBUG] Lowercase: {repr(message.text.lower())}")
            print(f"🔍 [GLOBAL DEBUG] Type: {type(message.text)}")
            print(f"🔍 [GLOBAL DEBUG] Length: {len(message.text) if message.text else 'None'}")
            
            logger.warning(f"🚨 UNHANDLED MESSAGE: '{message.text}' from user {message.from_user.id}")
            logger.warning(f"🚨 No specific handler matched this message")
            
            try:
                await message.reply(
                    f"🔍 Debug: Received '{message.text}'\n"
                    f"❌ No matching handler found\n"
                    f"💡 Try: /start, /help, or use menu buttons"
                )
                logger.info("✅ Global debug reply sent")
            except Exception as e:
                logger.error(f"❌ Failed to send debug reply: {e}")
        
        logger.info("✅ Global debug handler registered (lowest priority)")
        logger.info("🎯 All handlers registered successfully")
        
        logger.info("🤖 Bot is ready to start polling...")
        logger.info("=" * 60)
        
        # Start polling
        await dp.start_polling(
            bot,
            handle_signals=False,
            allowed_updates=dp.resolve_used_update_types()
        )
        
    except Exception as e:
        logger.error(f"💥 Fatal error in main function: {e}")
        logger.exception("📋 Full traceback:")
        raise

if __name__ == "__main__":
    try:
        logger.info("🚀 Bot startup initiated")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Bot crashed: {e}")
        logger.exception("📋 Full traceback:")
        raise
