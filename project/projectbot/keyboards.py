# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def start_survey_keyboard():
    keyboard = [
        [KeyboardButton(text="Пройти опрос")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def mood_keyboard():
    keyboard = [
        [KeyboardButton(text="Отлично 😀"), KeyboardButton(text="Хорошо 🙂"), 
         KeyboardButton(text="Нормально 😌"), KeyboardButton(text="Плохо 😟")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def motivation_keyboard():
    keyboard = [
        [KeyboardButton(text="Очень высокая 😀"), KeyboardButton(text="Высокая 🙂"), 
         KeyboardButton(text="Средняя 😌"), KeyboardButton(text="Низкая 😟"), 
         KeyboardButton(text="Очень низкая 😞")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def problem_keyboard():
    keyboard = [
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )