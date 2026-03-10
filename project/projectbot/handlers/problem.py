"""Problem submission handlers."""
import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from states.problem_states import ProblemFlow
from keyboards.problem import problem_severity_keyboard, meeting_needed_keyboard
from keyboards.main_menu import main_menu_keyboard
from services.problem_service import save_problem
from services.user_service import register_user

logger = logging.getLogger(__name__)
router = Router()


@router.message(StateFilter(None), F.text.contains("проблем"))
async def start_problem_flow(message: types.Message, state: FSMContext) -> None:
    """Start problem submission flow - only when NOT in any state."""
    logger.info(f"🚨 [PROBLEM START] User {message.from_user.id}, text: '{message.text}'")
    
    await register_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )
    
    await message.answer(
        "🚨 Насколько критична проблема?",
        reply_markup=problem_severity_keyboard()
    )
    await state.set_state(ProblemFlow.severity)
    logger.info(f"   → State set to: severity")


@router.message(ProblemFlow.severity, F.text.in_([
    "🚨 Критическая проблема", "⚠️ Серьезная проблема",
    "❗️ Умеренная проблема", "⚡️ Малозначительная проблема", "🔧 Мелкая проблема"
]))
async def process_severity(message: types.Message, state: FSMContext) -> None:
    """Process problem severity selection."""
    logger.info(f"📝 [SEVERITY] User {message.from_user.id}, selected: '{message.text}'")
    await state.update_data(severity=message.text)
    await message.answer("📝 Опиши кратко проблему")
    await state.set_state(ProblemFlow.description)
    logger.info(f"   → State set to: description")


@router.message(ProblemFlow.description)
async def process_description(message: types.Message, state: FSMContext) -> None:
    """Process problem description."""
    logger.info(f"📝 [DESCRIPTION] User {message.from_user.id}, text: '{message.text}'")
    await state.update_data(description=message.text)
    await message.answer("🤝 Нужна ли встреча?", reply_markup=meeting_needed_keyboard())
    await state.set_state(ProblemFlow.meeting_needed)
    logger.info(f"   → State set to: meeting_needed")


@router.message(ProblemFlow.meeting_needed, F.text.in_(["Да", "Нет"]))
async def process_meeting(message: types.Message, state: FSMContext) -> None:
    """Process meeting needed selection and save problem."""
    data = await state.get_data()
    
    logger.info(f"💾 [SAVE] User {message.from_user.id}, meeting: '{message.text}'")
    logger.info(f"   Data: severity={data.get('severity')}, description={data.get('description')}")
    
    await save_problem(
        user_id=message.from_user.id,
        severity=data.get("severity"),
        description=data.get("description"),
        meeting_needed=message.text
    )
    
    await message.answer(
        "✅ Проблема сохранена! Мы рассмотрим ее в ближайшее время.",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()
    logger.info(f"   → Flow completed, state cleared")
