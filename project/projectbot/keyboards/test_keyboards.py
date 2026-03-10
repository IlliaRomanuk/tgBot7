# keyboards/test_keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def test_keyboard():
    """Test button for daily survey"""
    keyboard = [
        [KeyboardButton(text="➡️ Пройти тест")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def mood_keyboard():
    """Mood selection keyboard"""
    keyboard = [
        [KeyboardButton(text="😀 Отлично"), KeyboardButton(text="🙂 Хорошо")],
        [KeyboardButton(text="😐 Нормально"), KeyboardButton(text="😟 Плохо")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def motivation_keyboard():
    """Motivation selection keyboard"""
    keyboard = [
        [KeyboardButton(text="😀 Очень высокая"), KeyboardButton(text="🙂 Высокая")],
        [KeyboardButton(text="😐 Средняя"), KeyboardButton(text="😟 Низкая")],
        [KeyboardButton(text="😞 Очень низкая")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def problem_keyboard():
    """Problem selection keyboard"""
    keyboard = [
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
