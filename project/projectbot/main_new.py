"""Main entry point for the Telegram bot."""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, DEBUG_MODE
from handlers import start_router, idea_router, problem_router, test_router, debug_router
from database import init_db
from scheduler import setup_scheduler

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Main bot entry point."""
    logger.info("🚀 Starting Telegram Bot...")
    
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    logger.info(f"✅ Bot initialized with token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-4:]}")
    
    # Initialize database
    await init_db()
    logger.info("✅ Database initialized")
    
    # Setup scheduler
    scheduler = setup_scheduler(bot)
    scheduler.start()
    logger.info("✅ Scheduler started")
    
    # Register routers in priority order
    logger.info("🔗 Registering routers...")
    
    dp.include_router(start_router)
    dp.include_router(test_router)
    dp.include_router(idea_router)
    dp.include_router(problem_router)
    dp.include_router(debug_router)  # Must be last
    
    # Startup diagnostics
    logger.info("📊 Startup diagnostics:")
    logger.info(f"   Registered routers: {[r.name for r in dp.sub_routers]}")
    logger.info(f"   Update types: {dp.resolve_used_update_types()}")
    
    logger.info("✅ All systems ready. Starting polling...")
    
    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Bot stopped by user")
    except Exception as e:
        logger.exception(f"💥 Bot crashed: {e}")
        raise
