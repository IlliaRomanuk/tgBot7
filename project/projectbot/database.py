# database.py
import aiosqlite
import logging
from config import DB_FULL_PATH

logger = logging.getLogger(__name__)

async def init_db():
    """Initialize database with proper error handling"""
    try:
        logger.info(f"Initializing database at: {DB_FULL_PATH}")
        async with aiosqlite.connect(DB_FULL_PATH) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question TEXT,
                answer TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            await db.commit()
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.exception("Full traceback:")
        raise

async def save_response(user_id, question, answer):
    """Save response with error handling"""
    try:
        async with aiosqlite.connect(DB_FULL_PATH) as db:
            await db.execute(
                "INSERT INTO responses (user_id, question, answer) VALUES (?, ?, ?)",
                (user_id, question, answer)
            )
            await db.commit()
            logger.info(f"Response saved: user_id={user_id}, question={question}")
    except Exception as e:
        logger.error(f"Failed to save response: {e}")
        logger.exception("Full traceback:")
        # Don't raise - allow bot to continue working

async def get_users():
    """Get users with error handling"""
    try:
        async with aiosqlite.connect(DB_FULL_PATH) as db:
            async with db.execute("SELECT DISTINCT user_id FROM responses") as cursor:
                users = await cursor.fetchall()
                user_list = [u[0] for u in users]
                logger.info(f"Retrieved {len(user_list)} users from database")
                return user_list
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        logger.exception("Full traceback:")
        return []  # Return empty list to allow bot to continue