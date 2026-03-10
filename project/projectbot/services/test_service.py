"""Test service for saving test responses."""
import logging
from database import save_response as db_save_response

logger = logging.getLogger(__name__)


async def save_test_response(user_id: int, question: str, answer: str) -> None:
    """Save test response to database."""
    await db_save_response(user_id, question, answer)
    logger.info(f"Test response saved for user {user_id}: {question}")
