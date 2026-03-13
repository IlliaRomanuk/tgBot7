"""Configuration module - loads settings from environment variables."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
# On production server, variables are set directly in the environment
load_dotenv()


# =============================================================================
# BOT CONFIGURATION
# =============================================================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")


# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
DB_PATH = os.getenv("DB_PATH", "data/responses.db")
DB_FULL_PATH = os.path.join(os.getcwd(), DB_PATH)

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_FULL_PATH) if os.path.dirname(DB_PATH) else ".", exist_ok=True)


# =============================================================================
# SCHEDULER CONFIGURATION
# =============================================================================
DAILY_SURVEY_HOUR = int(os.getenv("DAILY_SURVEY_HOUR", "18"))
DAILY_SURVEY_MINUTE = int(os.getenv("DAILY_SURVEY_MINUTE", "0"))
SURVEY_TIME = (DAILY_SURVEY_HOUR, DAILY_SURVEY_MINUTE)


# =============================================================================
# DEBUG CONFIGURATION
# =============================================================================
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() in ("true", "1", "yes", "on")


# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO" if not DEBUG_MODE else "DEBUG")