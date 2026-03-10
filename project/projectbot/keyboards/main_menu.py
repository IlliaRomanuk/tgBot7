# keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    """Main menu keyboard with two buttons"""
    keyboard = [
        [KeyboardButton(text="Предложить идею")],
        [KeyboardButton(text="Сообщить о проблеме")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
