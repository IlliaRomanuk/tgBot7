# config.py
import os

# Bot configuration
BOT_TOKEN = "8079978673:AAGHAnkHIjmlgFoa--KbFINYmMugmq8bwWg"
DB_PATH = "responses.db"
DB_FULL_PATH = os.path.join(os.getcwd(), DB_PATH)

# Survey configuration
DAILY_SURVEY_HOUR = 18
DAILY_SURVEY_MINUTE = 0
SURVEY_TIME = (DAILY_SURVEY_HOUR, DAILY_SURVEY_MINUTE)

# Debug configuration
DEBUG_MODE = True