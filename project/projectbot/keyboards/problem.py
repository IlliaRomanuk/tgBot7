"""Problem submission keyboards."""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def problem_severity_keyboard() -> ReplyKeyboardMarkup:
    """Problem severity selection keyboard."""
    keyboard = [
        [KeyboardButton(text="🚨 Критическая проблема")],
        [KeyboardButton(text="⚠️ Серьезная проблема")],
        [KeyboardButton(text="❗️ Умеренная проблема")],
        [KeyboardButton(text="⚡️ Малозначительная проблема")],
        [KeyboardButton(text="🔧 Мелкая проблема")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def meeting_needed_keyboard() -> ReplyKeyboardMarkup:
    """Meeting needed selection keyboard."""
    keyboard = [
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
