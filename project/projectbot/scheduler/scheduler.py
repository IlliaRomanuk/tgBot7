"""Scheduler for daily test reminders."""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)


def setup_scheduler(bot=None):
    """Setup scheduler for daily test at 18:00."""
    try:
        scheduler = AsyncIOScheduler()
        
        # Import here to avoid circular imports
        from handlers.test import send_daily_test
        
        # Schedule daily test at 18:00 (6 PM)
        scheduler.add_job(
            send_daily_test,
            CronTrigger(hour=18, minute=00),
            id='daily_test',
            name='Daily Test',
            replace_existing=True,
            args=[bot] if bot else []
        )
        
        logger.info("Scheduler configured for daily test at 18:00")
        return scheduler
        
    except Exception as e:
        logger.error(f"Failed to setup scheduler: {e}")
        raise
