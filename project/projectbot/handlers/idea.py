"""Idea submission handlers."""
import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardRemove

from states.idea_states import IdeaFlow
from keyboards.idea import idea_priority_keyboard, idea_type_keyboard
from keyboards.main_menu import main_menu_keyboard
from services.idea_service import save_idea
from services.user_service import register_user

logger = logging.getLogger(__name__)
router = Router()


@router.message(StateFilter(None), F.text == "Предложить идею")
async def start_idea_flow(message: types.Message, state: FSMContext) -> None:
    """Start idea submission flow."""
    logger.info(f"💡 [IDEA START] User {message.from_user.id} pressed 'Предложить идею'")
    
    await register_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )
    
    await message.answer(
        "🎯 Выберите приоритет идеи:",
        reply_markup=idea_priority_keyboard()
    )
    await state.set_state(IdeaFlow.priority)


@router.message(IdeaFlow.priority, F.text.in_([
    "🌟 Высший", "🔥 Высокий", "💡 Средний", "🌱 Низкий", "⏳ Минимальный"
]))
async def process_priority(message: types.Message, state: FSMContext) -> None:
    """Process idea priority selection."""
    logger.info(f"Idea priority selected: {message.text}")
    await state.update_data(priority=message.text)
    await message.answer("📋 Какого рода идея?", reply_markup=idea_type_keyboard())
    await state.set_state(IdeaFlow.idea_type)


@router.message(IdeaFlow.idea_type, F.text.in_(["улучшение работы", "новое направление"]))
async def process_type(message: types.Message, state: FSMContext) -> None:
    """Process idea type selection."""
    logger.info(f"Idea type selected: {message.text}")
    await state.update_data(idea_type=message.text)
    await message.answer(
        "✍️ Опиши свою идею",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(IdeaFlow.description)


@router.message(IdeaFlow.description)
async def process_description(message: types.Message, state: FSMContext) -> None:
    """Process idea description and save to database."""
    data = await state.get_data()
    
    logger.info(f"Saving idea from user {message.from_user.id}")
    await save_idea(
        user_id=message.from_user.id,
        priority=data.get("priority"),
        idea_type=data.get("idea_type"),
        description=message.text
    )
    
    await message.answer(
        "✅ Идея сохранена! Спасибо за предложение.",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()
