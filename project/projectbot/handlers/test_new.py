"""Test flow handlers."""
import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from states.test_states import TestFlow
from keyboards.test import test_keyboard, mood_keyboard, motivation_keyboard, problem_keyboard
from keyboards.main_menu import main_menu_keyboard
from services.test_service import save_test_response

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text == "➡️ Пройти тест")
async def start_test(message: types.Message, state: FSMContext) -> None:
    """Start daily test flow."""
    logger.info(f"User {message.from_user.id} started test")
    await state.set_state(TestFlow.mood)
    await message.answer(
        "😊 Каково твое настроение сегодня?",
        reply_markup=mood_keyboard()
    )


@router.message(TestFlow.mood, F.text.in_(["😀 Отлично", "🙂 Хорошо", "😐 Нормально", "😟 Плохо"]))
async def process_mood(message: types.Message, state: FSMContext) -> None:
    """Process mood response."""
    await state.update_data(mood=message.text)
    await save_test_response(message.from_user.id, "mood", message.text)
    await state.set_state(TestFlow.motivation)
    await message.answer(
        "💪 Какова твоя мотивация?",
        reply_markup=motivation_keyboard()
    )


@router.message(TestFlow.motivation, F.text.in_([
    "😀 Очень высокая", "🙂 Высокая", "😐 Средняя", "😟 Низкая", "😞 Очень низкая"
]))
async def process_motivation(message: types.Message, state: FSMContext) -> None:
    """Process motivation response."""
    await state.update_data(motivation=message.text)
    await save_test_response(message.from_user.id, "motivation", message.text)
    await state.set_state(TestFlow.problems)
    await message.answer(
        "🤔 Возникли ли проблемы на работе?",
        reply_markup=problem_keyboard()
    )


@router.message(TestFlow.problems, F.text.in_(["Да", "Нет"]))
async def process_problems(message: types.Message, state: FSMContext) -> None:
    """Process problems response and complete test."""
    await state.update_data(problems=message.text)
    await save_test_response(message.from_user.id, "problems", message.text)
    await message.answer(
        "✅ Тест завершен! Спасибо за участие.",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()
