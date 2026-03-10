"""User service for user registration."""
import logging
from database import register_user as db_register_user

logger = logging.getLogger(__name__)


async def register_user(user_id: int, username: str | None, first_name: str | None, last_name: str | None) -> None:
    """Register or update user in database."""
    await db_register_user(user_id, username, first_name, last_name)
    logger.info(f"User {user_id} registered/updated")
