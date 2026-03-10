"""Idea service for saving ideas."""
import logging
from database import save_idea as db_save_idea

logger = logging.getLogger(__name__)


async def save_idea(user_id: int, priority: str, idea_type: str, description: str) -> None:
    """Save idea to database."""
    await db_save_idea(user_id, priority, idea_type, description)
    logger.info(f"Idea saved for user {user_id}")
