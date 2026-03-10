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
            # Original responses table (keep for compatibility)
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
            
            # Users table for tracking registered users
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
        logger.exception("Full traceback:")
        raise

async def save_response(user_id, question, answer):
    """Save response with error handling (legacy function)"""
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

async def save_idea(user_id, priority, idea_type, description):
    """Save idea with error handling"""
    try:
        async with aiosqlite.connect(DB_FULL_PATH) as db:
            await db.execute(
                "INSERT INTO ideas (user_id, priority, type, description) VALUES (?, ?, ?, ?)",
                (user_id, priority, idea_type, description)
            )
            await db.commit()
            logger.info(f"Idea saved: user_id={user_id}, priority={priority}, type={idea_type}")
    except Exception as e:
        logger.error(f"Failed to save idea: {e}")
        logger.exception("Full traceback:")
        raise

async def save_problem(user_id, severity, description, meeting_needed):
    """Save problem with error handling"""
    try:
        async with aiosqlite.connect(DB_FULL_PATH) as db:
            await db.execute(
                "INSERT INTO problems (user_id, severity, description, meeting_needed) VALUES (?, ?, ?, ?)",
                (user_id, severity, description, meeting_needed)
            )
            await db.commit()
            logger.info(f"Problem saved: user_id={user_id}, severity={severity}, meeting_needed={meeting_needed}")
    except Exception as e:
        logger.error(f"Failed to save problem: {e}")
        logger.exception("Full traceback:")
        raise

async def register_user(user_id, username, first_name, last_name):
    """Register user in database"""
    try:
        async with aiosqlite.connect(DB_FULL_PATH) as db:
            await db.execute(
                "INSERT OR REPLACE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
                (user_id, username, first_name, last_name)
            )
            await db.commit()
            logger.info(f"User registered: user_id={user_id}, username={username}")
    except Exception as e:
        logger.error(f"Failed to register user: {e}")
        logger.exception("Full traceback:")
        # Don't raise - allow bot to continue working

async def get_users():
    """Get all registered users with error handling"""
    try:
        async with aiosqlite.connect(DB_FULL_PATH) as db:
            async with db.execute("SELECT user_id FROM users") as cursor:
                users = await cursor.fetchall()
                user_list = [u[0] for u in users]
                logger.info(f"Retrieved {len(user_list)} users from database")
                return user_list
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        logger.exception("Full traceback:")
        return []  # Return empty list to allow bot to continue

async def get_ideas():
    """Get all ideas for reporting"""
    try:
        async with aiosqlite.connect(DB_FULL_PATH) as db:
            async with db.execute("""
                SELECT user_id, priority, type, description, date 
                FROM ideas 
                ORDER BY date DESC
            """) as cursor:
                ideas = await cursor.fetchall()
                logger.info(f"Retrieved {len(ideas)} ideas from database")
                return ideas
    except Exception as e:
        logger.error(f"Failed to get ideas: {e}")
        logger.exception("Full traceback:")
        return []

async def get_problems():
    """Get all problems for reporting"""
    try:
        async with aiosqlite.connect(DB_FULL_PATH) as db:
            async with db.execute("""
                SELECT user_id, severity, description, meeting_needed, date 
                FROM problems 
                ORDER BY date DESC
            """) as cursor:
                problems = await cursor.fetchall()
                logger.info(f"Retrieved {len(problems)} problems from database")
                return problems
    except Exception as e:
        logger.error(f"Failed to get problems: {e}")
        logger.exception("Full traceback:")
        return []