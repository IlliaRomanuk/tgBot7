# handlers/start.py
import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards import start_survey_keyboard

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    """Handle /start command with logging and error handling"""
    try:
        logger.info(f"User {message.from_user.id} ({message.from_user.username}) started the bot")
        await message.answer(
            "Благодарим тебя за рабочий день! Мы рады, что ты являешься частью нашей команды.\n"
            "Нам важно отслеживать настроение и мотивацию сотрудников.\n"
            "Ты будешь получать опрос каждый день в 18:00.",
            reply_markup=start_survey_keyboard()
        )
        logger.info(f"Welcome message sent to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in start handler for user {message.from_user.id}: {e}")
        try:
            await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
        except:
            logger.error("Failed to send error message to user")

@router.message(Command("help"))
async def help_command(message: types.Message):
    """Handle /help command with logging and error handling"""
    try:
        logger.info(f"User {message.from_user.id} requested help")
        help_text = """
📋 **Доступные команды:**

/start - Начать работу с ботом
/help - Показать это сообщение
/idea - Поделиться идеей
/problem - Сообщить о проблеме

📊 **Опросы:**
"Пройти опрос" - Начать ежедневный опрос о настроении и мотивации

Спасибо за участие! 🎉
        """
        await message.answer(help_text, parse_mode="Markdown")
        logger.info(f"Help message sent to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in help handler for user {message.from_user.id}: {e}")
        try:
            await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
        except:
            logger.error("Failed to send error message to user")

def register_start_handlers(dp):
    """Register start handlers with logging"""
    try:
        dp.include_router(router)
        logger.info("Start handlers registered successfully")
    except Exception as e:
        logger.error(f"Failed to register start handlers: {e}")
        raise