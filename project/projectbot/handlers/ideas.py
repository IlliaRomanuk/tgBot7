# handlers/ideas.py
import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from database import save_response

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("idea", "problem"))
async def handle_idea(message: types.Message):
    """Handle idea/problem commands with logging and error handling"""
    try:
        logger.info(f"User {message.from_user.id} initiated idea/problem submission")
        await message.answer("Опишите вашу идею или проблему. Мы обязательно рассмотрим её.")
        logger.info(f"Idea/problem prompt sent to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in handle_idea for user {message.from_user.id}: {e}")
        try:
            await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
        except:
            logger.error("Failed to send error message to user")

@router.message(F.reply_to_message & (F.reply_to_message.text == "Опишите вашу идею или проблему. Мы обязательно рассмотрим её."))
async def save_idea(message: types.Message):
    """Handle idea/problem submission with logging and error handling"""
    try:
        logger.info(f"User {message.from_user.id} submitted idea/problem: {message.text[:50]}...")
        await save_response(message.from_user.id, "Идея/Проблема", message.text)
        await message.answer("Спасибо! Ваша идея/проблема была сохранена и будет рассмотрена.")
        logger.info(f"Idea/problem saved for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in save_idea for user {message.from_user.id}: {e}")
        try:
            await message.answer("Произошла ошибка при сохранении. Пожалуйста, попробуйте еще раз.")
        except:
            logger.error("Failed to send error message to user")

def register_idea_handlers(dp):
    """Register idea handlers with logging"""
    try:
        dp.include_router(router)
        logger.info("Idea handlers registered successfully")
    except Exception as e:
        logger.error(f"Failed to register idea handlers: {e}")
        raise