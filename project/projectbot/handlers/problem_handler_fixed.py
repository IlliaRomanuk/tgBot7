# handlers/problem_handler.py
import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.problem_states import ProblemFlow
from keyboards.problem_keyboards import problem_severity_keyboard, meeting_needed_keyboard
from keyboards.main_menu import main_menu_keyboard
from database import save_problem, register_user

logger = logging.getLogger(__name__)
router = Router()

# FIXED: Robust filter for problem button - handles variations and case-insensitive
@router.message(F.text.lower().contains("проблем"))
async def start_problem_flow(message: types.Message, state: FSMContext):
    """Start problem submission flow - FIXED: Robust filter for variations"""
    try:
        logger.info(f"🚨 User {message.from_user.id} started problem flow")
        logger.info(f"Message text: '{message.text}'")
        logger.info(f"Current state before: {await state.get_state()}")
        
        # Register user
        await register_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
        logger.info("User registered successfully")
        
        # Send severity selection and set FSM state
        await message.answer("Насколько критична твоя проблема?", reply_markup=problem_severity_keyboard())
        await state.set_state(ProblemFlow.severity)
        logger.info(f"✅ Problem severity selection sent, state set to: {await state.get_state()}")
        
    except Exception as e:
        logger.error(f"❌ Error in start_problem_flow: {e}")
        logger.exception("Full traceback:")
        try:
            await message.answer("Произошла ошибка.", reply_markup=main_menu_keyboard())
            await state.clear()
        except Exception as inner_e:
            logger.error(f"❌ Failed to send error message: {inner_e}")

@router.message(ProblemFlow.severity, F.text.in_(["🚨 Критическая проблема", "⚠️ Серьезная проблема", "❗️ Умеренная проблема", "⚡️ Малозначительная проблема", "🔧 Мелкая проблема"]))
async def process_problem_severity(message: types.Message, state: FSMContext):
    """Process problem severity selection"""
    try:
        logger.info(f"Processing problem severity: {message.text}")
        logger.info(f"Current state: {await state.get_state()}")
        
        await state.update_data(severity=message.text)
        logger.info("Severity saved to state")
        
        await message.answer("Опиши кратко трудности или проблемы, с которыми ты столкнулся")
        await state.set_state(ProblemFlow.description)
        logger.info(f"✅ Problem description request sent, new state: {await state.get_state()}")
        
    except Exception as e:
        logger.error(f"❌ Error in process_problem_severity: {e}")
        logger.exception("Full traceback:")
        try:
            await message.answer("Произошла ошибка.", reply_markup=main_menu_keyboard())
            await state.clear()
        except Exception as inner_e:
            logger.error(f"❌ Failed to send error message: {inner_e}")

@router.message(ProblemFlow.description)
async def process_problem_description(message: types.Message, state: FSMContext):
    """Process problem description"""
    try:
        logger.info(f"Processing problem description: {message.text[:50]}...")
        logger.info(f"Current state: {await state.get_state()}")
        
        await state.update_data(description=message.text)
        logger.info("Description saved to state")
        
        await message.answer("Нужна ли тебе встреча?", reply_markup=meeting_needed_keyboard())
        await state.set_state(ProblemFlow.meeting_needed)
        logger.info(f"✅ Meeting needed selection sent, new state: {await state.get_state()}")
        
    except Exception as e:
        logger.error(f"❌ Error in process_problem_description: {e}")
        logger.exception("Full traceback:")
        try:
            await message.answer("Произошла ошибка.", reply_markup=main_menu_keyboard())
            await state.clear()
        except Exception as inner_e:
            logger.error(f"❌ Failed to send error message: {inner_e}")

@router.message(ProblemFlow.meeting_needed, F.text.in_(["Да", "Нет"]))
async def process_meeting_needed(message: types.Message, state: FSMContext):
    """Process meeting needed selection"""
    try:
        logger.info(f"Processing meeting needed: {message.text}")
        logger.info(f"Current state: {await state.get_state()}")
        
        data = await state.get_data()
        await save_problem(
            message.from_user.id,
            data.get('severity'),
            data.get('description'),
            message.text
        )
        logger.info("Problem saved to database")
        
        await message.answer("Информация о проблеме отправлена.", reply_markup=main_menu_keyboard())
        await state.clear()
        logger.info("✅ Problem flow completed successfully")
        logger.info(f"Final state: {await state.get_state()}")
        
    except Exception as e:
        logger.error(f"❌ Error in process_meeting_needed: {e}")
        logger.exception("Full traceback:")
        try:
            await message.answer("Произошла ошибка.", reply_markup=main_menu_keyboard())
            await state.clear()
        except Exception as inner_e:
            logger.error(f"❌ Failed to send error message: {inner_e}")

# FIXED: No debug handler here - moved to global handler in main.py to prevent interference
