# handlers/daily_test.py
import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards import mood_keyboard, motivation_keyboard, problem_keyboard, start_survey_keyboard
from database import save_response, get_users
from bot_instance import bot

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "📊 Пройти тест")
async def start_test(message: types.Message):
    """Handle test command with logging"""
    try:
        logger.info(f"User {message.from_user.id} started test")
        await message.answer("Вопрос дня: Что такое Python?")
    except Exception as e:
        logger.error(f"Error in start_test for user {message.from_user.id}: {e}")

@router.message(F.text == "Пройти опрос")
async def start_survey(message: types.Message):
    """Handle survey start with logging and error handling"""
    try:
        logger.info(f"User {message.from_user.id} started daily survey")
        await message.answer("Каково твое общее настроение сегодня?", reply_markup=mood_keyboard())
        logger.info(f"Mood keyboard sent to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in start_survey for user {message.from_user.id}: {e}")
        try:
            await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
        except:
            logger.error("Failed to send error message to user")

@router.message(F.text.in_(["Отлично 😀", "Хорошо 🙂", "Нормально 😌", "Плохо 😟"]))
async def mood_handler(message: types.Message):
    """Handle mood response with logging and error handling"""
    try:
        logger.info(f"User {message.from_user.id} selected mood: {message.text}")
        await save_response(message.from_user.id, "Настроение", message.text)
        await message.answer("Как ты оцениваешь свою мотивацию на работе сегодня?", reply_markup=motivation_keyboard())
        logger.info(f"Motivation keyboard sent to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in mood_handler for user {message.from_user.id}: {e}")
        try:
            await message.answer("Произошла ошибка при сохранении ответа. Пожалуйста, попробуйте еще раз.")
        except:
            logger.error("Failed to send error message to user")

@router.message(F.text.in_(["Очень высокая 😀", "Высокая 🙂", "Средняя 😌", "Низкая 😟", "Очень низкая 😞"]))
async def motivation_handler(message: types.Message):
    """Handle motivation response with logging and error handling"""
    try:
        logger.info(f"User {message.from_user.id} selected motivation: {message.text}")
        await save_response(message.from_user.id, "Мотивация", message.text)
        await message.answer("Возникли ли у тебя какие-либо проблемы во время рабочего дня?", reply_markup=problem_keyboard())
        logger.info(f"Problem keyboard sent to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in motivation_handler for user {message.from_user.id}: {e}")
        try:
            await message.answer("Произошла ошибка при сохранении ответа. Пожалуйста, попробуйте еще раз.")
        except:
            logger.error("Failed to send error message to user")

@router.message(F.text.in_(["Да", "Нет"]))
async def problem_handler(message: types.Message):
    """Handle problem response with logging and error handling"""
    try:
        logger.info(f"User {message.from_user.id} answered problem question: {message.text}")
        await save_response(message.from_user.id, "Проблемы", message.text)
        if message.text == "Да":
            await message.answer("Опишите, пожалуйста, проблему:")
            logger.info(f"Problem description requested from user {message.from_user.id}")
        else:
            await message.answer("Спасибо за прохождение опроса!", reply_markup=start_survey_keyboard())
            logger.info(f"Survey completed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in problem_handler for user {message.from_user.id}: {e}")
        try:
            await message.answer("Произошла ошибка при сохранении ответа. Пожалуйста, попробуйте еще раз.")
        except:
            logger.error("Failed to send error message to user")

# Ежедневная рассылка
async def send_daily_survey():
    """Send daily survey with logging and error handling"""
    try:
        users = await get_users()
        logger.info(f"Starting daily survey for {len(users)} users")
        for user_id in users:
            try:
                await bot.send_message(user_id, "Привет! Пора пройти ежедневный опрос.",
                                       reply_markup=start_survey_keyboard())
                logger.info(f"Daily survey sent to user {user_id}")
            except Exception as e:
                logger.error(f"Failed to send daily survey to user {user_id}: {e}")
                continue
        logger.info("Daily survey sending completed")
    except Exception as e:
        logger.error(f"Error in send_daily_survey: {e}")

def register_daily_test_handlers(dp):
    """Register daily test handlers with logging"""
    try:
        dp.include_router(router)
        logger.info("Daily test handlers registered successfully")
    except Exception as e:
        logger.error(f"Failed to register daily test handlers: {e}")
        raise