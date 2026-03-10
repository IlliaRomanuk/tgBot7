"""Problem service for saving problems."""
import logging
from database import save_problem as db_save_problem

logger = logging.getLogger(__name__)


async def save_problem(user_id: int, severity: str, description: str, meeting_needed: str) -> None:
    """Save problem to database."""
    await db_save_problem(user_id, severity, description, meeting_needed)
    logger.info(f"Problem saved for user {user_id}")
