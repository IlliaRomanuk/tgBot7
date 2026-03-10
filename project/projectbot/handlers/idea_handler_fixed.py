# handlers/idea_handler.py
import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.idea_states import IdeaFlow
from keyboards.idea_keyboards import idea_priority_keyboard, idea_type_keyboard
from keyboards.main_menu import main_menu_keyboard
from database import save_idea, register_user

logger = logging.getLogger(__name__)
router = Router()

# FIXED: Robust filter for idea button - handles variations and case-insensitive
@router.message(F.text.lower().contains("иде"))
async def start_idea_flow(message: types.Message, state: FSMContext):
    """Start idea submission flow - FIXED: Robust filter for variations"""
    try:
        logger.info(f"💡 User {message.from_user.id} started idea flow")
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
        
        # Send priority selection and set FSM state
        await message.answer("Выберите приоритет идеи:", reply_markup=idea_priority_keyboard())
        await state.set_state(IdeaFlow.priority)
        logger.info(f"✅ Idea priority selection sent, state set to: {await state.get_state()}")
        
    except Exception as e:
        logger.error(f"❌ Error in start_idea_flow: {e}")
        logger.exception("Full traceback:")
        try:
            await message.answer("Произошла ошибка.", reply_markup=main_menu_keyboard())
            await state.clear()
        except Exception as inner_e:
            logger.error(f"❌ Failed to send error message: {inner_e}")

@router.message(IdeaFlow.priority, F.text.in_(["🌟 Высший", "🔥 Высокий", "💡 Средний", "🌱 Низкий", "⏳ Минимальный"]))
async def process_idea_priority(message: types.Message, state: FSMContext):
    """Process idea priority selection"""
    try:
        logger.info(f"Processing idea priority: {message.text}")
        logger.info(f"Current state: {await state.get_state()}")
        
        await state.update_data(priority=message.text)
        logger.info("Priority saved to state")
        
        await message.answer("Какого рода идея?", reply_markup=idea_type_keyboard())
        await state.set_state(IdeaFlow.idea_type)
        logger.info(f"✅ Idea type selection sent, new state: {await state.get_state()}")
        
    except Exception as e:
        logger.error(f"❌ Error in process_idea_priority: {e}")
        logger.exception("Full traceback:")
        try:
            await message.answer("Произошла ошибка.", reply_markup=main_menu_keyboard())
            await state.clear()
        except Exception as inner_e:
            logger.error(f"❌ Failed to send error message: {inner_e}")

@router.message(IdeaFlow.idea_type, F.text.in_(["улучшение работы", "новое направление"]))
async def process_idea_type(message: types.Message, state: FSMContext):
    """Process idea type selection"""
    try:
        logger.info(f"Processing idea type: {message.text}")
        logger.info(f"Current state: {await state.get_state()}")
        
        await state.update_data(type=message.text)
        logger.info("Type saved to state")
        
        await message.answer("Опиши свою идею")
        await state.set_state(IdeaFlow.description)
        logger.info(f"✅ Idea description request sent, new state: {await state.get_state()}")
        
    except Exception as e:
        logger.error(f"❌ Error in process_idea_type: {e}")
        logger.exception("Full traceback:")
        try:
            await message.answer("Произошла ошибка.", reply_markup=main_menu_keyboard())
            await state.clear()
        except Exception as inner_e:
            logger.error(f"❌ Failed to send error message: {inner_e}")

@router.message(IdeaFlow.description)
async def process_idea_description(message: types.Message, state: FSMContext):
    """Process idea description"""
    try:
        logger.info(f"Processing idea description: {message.text[:50]}...")
        logger.info(f"Current state: {await state.get_state()}")
        
        data = await state.get_data()
        await save_idea(
            message.from_user.id,
            data.get('priority'),
            data.get('type'),
            message.text
        )
        logger.info("Idea saved to database")
        
        await message.answer("Информация об идее отправлена.", reply_markup=main_menu_keyboard())
        await state.clear()
        logger.info("✅ Idea flow completed successfully")
        logger.info(f"Final state: {await state.get_state()}")
        
    except Exception as e:
        logger.error(f"❌ Error in process_idea_description: {e}")
        logger.exception("Full traceback:")
        try:
            await message.answer("Произошла ошибка.", reply_markup=main_menu_keyboard())
            await state.clear()
        except Exception as inner_e:
            logger.error(f"❌ Failed to send error message: {inner_e}")

# FIXED: No debug handler here - moved to global handler in main.py to prevent interference
