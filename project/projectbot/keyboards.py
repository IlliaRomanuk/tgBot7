# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    """Main menu keyboard with only two buttons"""
    keyboard = [
        [KeyboardButton(text="Предложить идею")],
        [KeyboardButton(text="Сообщить о проблеме")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

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

def problem_severity_keyboard():
    """Problem severity selection keyboard"""
    keyboard = [
        [KeyboardButton(text="🚨 Критическая проблема")],
        [KeyboardButton(text="⚠️ Серьезная проблема")],
        [KeyboardButton(text="❗️ Умеренная проблема")],
        [KeyboardButton(text="⚡️ Малозначительная проблема")],
        [KeyboardButton(text="🔧 Мелкая проблема")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def meeting_needed_keyboard():
    """Meeting needed selection keyboard"""
    keyboard = [
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def test_keyboard():
    """Test button for daily survey"""
    keyboard = [
        [KeyboardButton(text="➡️ Пройти тест")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

# Legacy keyboards - keep for compatibility but will be removed
def start_survey_keyboard():
    """Legacy keyboard - replaced by main_menu_keyboard"""
    return main_menu_keyboard()

def mood_keyboard():
    """Legacy keyboard - no longer used in main flow"""
    keyboard = [
        [KeyboardButton(text="Отлично 😀"), KeyboardButton(text="Хорошо �"), 
         KeyboardButton(text="Нормально 😌"), KeyboardButton(text="Плохо 😟")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def motivation_keyboard():
    """Legacy keyboard - no longer used in main flow"""
    keyboard = [
        [KeyboardButton(text="Очень высокая 😀"), KeyboardButton(text="Высокая �"), 
         KeyboardButton(text="Средняя 😌"), KeyboardButton(text="Низкая 😟"), 
         KeyboardButton(text="Очень низкая 😞")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def problem_keyboard():
    """Legacy keyboard - no longer used in main flow"""
    keyboard = [
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )