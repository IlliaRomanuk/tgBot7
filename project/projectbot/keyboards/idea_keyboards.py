# keyboards/idea_keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def idea_priority_keyboard():
    """Idea priority selection keyboard"""
    keyboard = [
        [KeyboardButton(text="🌟 Высший")],
        [KeyboardButton(text="🔥 Высокий")],
        [KeyboardButton(text="💡 Средний")],
        [KeyboardButton(text="🌱 Низкий")],
        [KeyboardButton(text="⏳ Минимальный")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def idea_type_keyboard():
    """Idea type selection keyboard"""
    keyboard = [
        [KeyboardButton(text="улучшение работы")],
        [KeyboardButton(text="новое направление")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
