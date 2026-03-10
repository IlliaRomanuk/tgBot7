# handlers/start_handler.py - WORKING VERSION
import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards.main_menu import main_menu_keyboard
from database import register_user

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    """Handle /start command"""
    print(f"🔍 [START COMMAND] Raw message: {repr(message.text)}")
    print(f"🔍 [START COMMAND] Type: {type(message.text)}")
    print(f"🔍 [START COMMAND] Length: {len(message.text) if message.text else 'None'}")
    
    try:
        logger.info(f"🚀 User {message.from_user.id} started the bot")
        logger.info(f"👤 Username: {message.from_user.username}, Name: {message.from_user.first_name}")
        
        # Register user
        await register_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
        logger.info("✅ User registered successfully")
        
        await message.answer(
            "👋 Добро пожаловать! Я бот для сбора идей и проблем. Выбери действие из меню ниже:",
            reply_markup=main_menu_keyboard()
        )
        logger.info(f"✅ Welcome message sent to user {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"❌ Error in start handler: {e}")
        logger.exception("📋 Full traceback:")
        await message.answer("❌ Произошла ошибка. Пожалуйста, попробуйте еще раз.")

@router.message(Command("help"))
async def help_command(message: types.Message):
    """Handle /help command"""
    print(f"🔍 [HELP COMMAND] Raw message: {repr(message.text)}")
    print(f"🔍 [HELP COMMAND] Type: {type(message.text)}")
    print(f"🔍 [HELP COMMAND] Length: {len(message.text) if message.text else 'None'}")
    
    try:
        logger.info(f"❓ User {message.from_user.id} requested help")
        
        help_text = """
📋 **Доступные команды:**

/start - Начать работу с ботом
/help - Показать это сообщение

📊 **Основные функции:**
"Предложить идею" - Поделиться идеей для улучшения работы
"Сообщить о проблеме" - Сообщить о возникших проблемах

🕐 **Ежедневный тест:**
Каждый день в 18:00 вам будет отправлен тест для оценки настроения и мотивации.

Спасибо за участие! 🎉
        """
        await message.answer(help_text, parse_mode="Markdown")
        logger.info(f"✅ Help message sent to user {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"❌ Error in help handler: {e}")
        logger.exception("📋 Full traceback:")
        await message.answer("❌ Произошла ошибка. Пожалуйста, попробуйте еще раз.")

print("✅ start_handler.py loaded - Router instance created")
print(f"🔧 Router: {router}")
print(f"🔧 Handlers: {[handler for handler in router.handlers.values()]}")
