"""Database module for SQLite operations."""
import aiosqlite
import logging
from config import DB_FULL_PATH

logger = logging.getLogger(__name__)


async def init_db():
    """Initialize database with proper error handling."""
    try:
        logger.info(f"Initializing database at: {DB_FULL_PATH}")
        async with aiosqlite.connect(DB_FULL_PATH) as db:
            # Responses table (legacy)
            await db.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question TEXT,
                answer TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Ideas table
            await db.execute("""
            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                priority TEXT,
                type TEXT,
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Problems table
            await db.execute("""
            CREATE TABLE IF NOT EXISTS problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                severity TEXT,
                description TEXT,
                meeting_needed TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Users table
            await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            await db.commit()
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def save_response(user_id: int, question: str, answer: str) -> None:
    """Save test response."""
    async with aiosqlite.connect(DB_FULL_PATH) as db:
        await db.execute(
            "INSERT INTO responses (user_id, question, answer) VALUES (?, ?, ?)",
            (user_id, question, answer)
        )
        await db.commit()
        logger.info(f"Response saved: user_id={user_id}, question={question}")


async def save_idea(user_id: int, priority: str, idea_type: str, description: str) -> None:
    """Save idea to database."""
    async with aiosqlite.connect(DB_FULL_PATH) as db:
        await db.execute(
            "INSERT INTO ideas (user_id, priority, type, description) VALUES (?, ?, ?, ?)",
            (user_id, priority, idea_type, description)
        )
        await db.commit()
        logger.info(f"Idea saved: user_id={user_id}, priority={priority}")


async def save_problem(user_id: int, severity: str, description: str, meeting_needed: str) -> None:
    """Save problem to database."""
    async with aiosqlite.connect(DB_FULL_PATH) as db:
        await db.execute(
            "INSERT INTO problems (user_id, severity, description, meeting_needed) VALUES (?, ?, ?, ?)",
            (user_id, severity, description, meeting_needed)
        )
        await db.commit()
        logger.info(f"Problem saved: user_id={user_id}, severity={severity}")


async def register_user(user_id: int, username: str | None, first_name: str | None, last_name: str | None) -> None:
    """Register user in database."""
    async with aiosqlite.connect(DB_FULL_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
            (user_id, username, first_name, last_name)
        )
        await db.commit()
        logger.info(f"User registered: user_id={user_id}, username={username}")


async def get_users() -> list[int]:
    """Get all registered users."""
    async with aiosqlite.connect(DB_FULL_PATH) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            users = await cursor.fetchall()
            return [u[0] for u in users]
