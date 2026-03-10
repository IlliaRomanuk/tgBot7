"""Start command handlers."""
import logging
from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main_menu import main_menu_keyboard
from services.user_service import register_user

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message) -> None:
    """Handle /start command."""
    logger.info(f"User {message.from_user.id} started the bot")
    
    await register_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )
    
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        f"Я бот для сбора обратной связи.\n"
        f"Используй меню ниже для взаимодействия.",
        reply_markup=main_menu_keyboard()
    )


@router.message(Command("help"))
async def help_command(message: types.Message) -> None:
    """Handle /help command."""
    logger.info(f"User {message.from_user.id} requested help")
    
    await message.answer(
        "ℹ️ <b>Помощь по боту</b>\n\n"
        "<b>Доступные команды:</b>\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку\n\n"
        "<b>Кнопки меню:</b>\n"
        "• Предложить идею - Отправить предложение\n"
        "• Сообщить о проблеме - Сообщить о проблеме\n"
        "• ➡️ Пройти тест - Пройти ежедневный тест"
    )