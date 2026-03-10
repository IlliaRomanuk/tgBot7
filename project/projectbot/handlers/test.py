"""Test flow handlers with daily test reminder."""
import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardRemove

from states.test_states import TestFlow
from keyboards.test import (
    test_keyboard, mood_keyboard, motivation_keyboard,
    problem_keyboard, test_problem_severity_keyboard
)
from keyboards.main_menu import main_menu_keyboard
from services.test_service import save_test_response
from database import get_users

logger = logging.getLogger(__name__)
router = Router()


@router.message(StateFilter(None), F.text == "➡️ Пройти тест")
async def start_test(message: types.Message, state: FSMContext) -> None:
    """Start daily test flow."""
    logger.info(f"🔥 [TEST START] User {message.from_user.id} pressed '➡️ Пройти тест'")
    await state.set_state(TestFlow.mood)
    await message.answer(
        "😊 Каково твое настроение сегодня?",
        reply_markup=mood_keyboard()
    )


@router.message(TestFlow.mood, F.text.in_(["😀 Отлично", "🙂 Хорошо", "😐 Нормально", "😟 Плохо"]))
async def process_mood(message: types.Message, state: FSMContext) -> None:
    """Process mood response."""
    logger.info(f"[TEST] Mood selected: {message.text}")
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
    logger.info(f"[TEST] Motivation selected: {message.text}")
    await state.update_data(motivation=message.text)
    await save_test_response(message.from_user.id, "motivation", message.text)
    await state.set_state(TestFlow.problems)
    await message.answer(
        "🤔 Возникли ли проблемы на работе?",
        reply_markup=problem_keyboard()
    )


@router.message(TestFlow.problems, F.text == "Нет")
async def process_problems_no(message: types.Message, state: FSMContext) -> None:
    """Process problems answer 'Нет' - end test immediately."""
    logger.info(f"[TEST] Problems answer: Нет - ending test")
    await state.update_data(problems=message.text)
    await save_test_response(message.from_user.id, "problems", message.text)
    await message.answer(
        "Спасибо за прохождение опроса",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()
    logger.info(f"[TEST] Test completed for user {message.from_user.id}")


@router.message(TestFlow.problems, F.text == "Да")
async def process_problems_yes(message: types.Message, state: FSMContext) -> None:
    """Process problems answer 'Да' - continue to severity selection."""
    logger.info(f"[TEST] Problems answer: Да - continuing to severity")
    await state.update_data(problems=message.text)
    await save_test_response(message.from_user.id, "problems", message.text)
    await state.set_state(TestFlow.problem_severity)
    await message.answer(
        "Насколько критична твоя проблема?\n\n"
        "🚨 Критическая проблема: нарушение ключевых функций или процессов.\n"
        "⚠️ Серьезная проблема: существенное влияние на производительность или качество.\n"
        "❗ Умеренная проблема: затрудняет выполнение задач, но не является критическим.\n"
        "⚡ Малозначительная проблема: слабое воздействие на рабочий процесс.\n"
        "🔧 Мелкая проблема: незначительное влияние на работу.",
        reply_markup=test_problem_severity_keyboard()
    )


@router.message(TestFlow.problem_severity, F.text.in_([
    "🚨 Критическая проблема", "⚠️ Серьезная проблема",
    "❗️ Умеренная проблема", "⚡️ Малозначительная проблема", "🔧 Мелкая проблема"
]))
async def process_problem_severity(message: types.Message, state: FSMContext) -> None:
    """Process problem severity selection in test flow."""
    logger.info(f"[TEST] Problem severity selected: {message.text}")
    await state.update_data(problem_severity=message.text)
    await state.set_state(TestFlow.problem_description)
    await message.answer(
        "Опиши кратко трудности или проблемы, с которыми ты столкнулся",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(TestFlow.problem_description)
async def process_problem_description(message: types.Message, state: FSMContext) -> None:
    """Process problem description in test flow."""
    logger.info(f"[TEST] Problem description received from user {message.from_user.id}")
    await state.update_data(problem_description=message.text)
    await state.set_state(TestFlow.problem_meeting)
    await message.answer(
        "Нужна ли тебе встреча?",
        reply_markup=problem_keyboard()
    )


@router.message(TestFlow.problem_meeting, F.text.in_(["Да", "Нет"]))
async def process_problem_meeting(message: types.Message, state: FSMContext) -> None:
    """Process meeting needed and complete test."""
    data = await state.get_data()
    logger.info(f"[TEST] Meeting needed: {message.text}, completing test")
    
    # Save all test data including problem details
    await save_test_response(message.from_user.id, "problem_meeting", message.text)
    
    await message.answer(
        "Спасибо за прохождение опроса",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()
    logger.info(f"[TEST] Test with problem flow completed for user {message.from_user.id}")


async def send_daily_test(bot) -> None:
    """Send daily test to all users."""
    users = await get_users()
    logger.info(f"Sending daily test to {len(users)} users")
    
    for user_id in users:
        try:
            await bot.send_message(
                user_id,
                "🔔 Пора пройти ежедневный тест!",
                reply_markup=test_keyboard()
            )
            logger.info(f"Test reminder sent to user {user_id}")
        except Exception as e:
            logger.error(f"Failed to send test to user {user_id}: {e}")
