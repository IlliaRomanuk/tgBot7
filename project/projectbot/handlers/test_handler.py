# handlers/test_handler.py - WORKING VERSION with diagnostics
import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.test_states import TestFlow
from keyboards.test_keyboards import test_keyboard, mood_keyboard, motivation_keyboard, problem_keyboard
from keyboards.main_menu import main_menu_keyboard
from database import save_response, get_users

logger = logging.getLogger(__name__)
router = Router()

@router.message(lambda m: m.text and "пройти" in m.text.lower())
async def start_test_flow(message: types.Message, state: FSMContext):
    """Start daily test flow"""
    print("🔥 TEST HANDLER TRIGGERED - FILTER MATCHED!")
    print(f"🔍 [TEST HANDLER] Raw message: {repr(message.text)}")
    print(f"🔍 [TEST HANDLER] Lowercase: {repr(message.text.lower())}")
    print(f"🔍 [TEST HANDLER] Contains 'пройти'? {'пройти' in message.text.lower()}")
    print(f"🔍 [TEST HANDLER] Type: {type(message.text)}")
    print(f"🔍 [TEST HANDLER] Length: {len(message.text) if message.text else 'None'}")
    
    try:
        logger.info(f"🔥 TEST BUTTON PRESSED by user {message.from_user.id}")
        logger.info(f"📝 Message text: '{message.text}'")
        logger.info(f"🔧 Current state before: {await state.get_state()}")
        
        # Set FSM state
        await state.set_state(TestFlow.mood)
        logger.info(f"✅ State after setting: {await state.get_state()}")
        
        # Send first question
        await message.answer(
            "😊 Каково твоё настроение сегодня?",
            reply_markup=mood_keyboard()
        )
        logger.info("✅ Test flow started successfully - mood question sent")
        
    except Exception as e:
        logger.error(f"❌ ERROR in start_test_flow: {e}")
        logger.exception("📋 Full traceback:")
        try:
            await message.answer(
                "❌ Произошла ошибка. Пожалуйста, попробуйте еще раз.",
                reply_markup=main_menu_keyboard()
            )
            await state.clear()
            logger.info("🧹 State cleared due to error")
        except Exception as inner_e:
            logger.error(f"❌ Failed to send error message: {inner_e}")

@router.message(TestFlow.mood, F.text.in_(["😀 Отлично", "🙂 Хорошо", "😐 Нормально", "😟 Плохо"]))
async def process_mood(message: types.Message, state: FSMContext):
    """Process mood response"""
    print("😊 MOOD HANDLER TRIGGERED!")
    print(f"🔍 [MOOD RESPONSE] Raw message: {repr(message.text)}")
    
    try:
        logger.info(f"😊 Processing mood: {message.text}")
        logger.info(f"🔧 Current state: {await state.get_state()}")
        
        # Save response
        await save_response(message.from_user.id, "Настроение", message.text)
        logger.info("💾 Mood response saved to database")
        
        # Set next state and send question
        await state.set_state(TestFlow.motivation)
        logger.info(f"✅ New state: {await state.get_state()}")
        
        await message.answer(
            "💪 Как ты оцениваешь свою мотивацию на работе сегодня?",
            reply_markup=motivation_keyboard()
        )
        logger.info("✅ Motivation question sent")
        
    except Exception as e:
        logger.error(f"❌ Error in process_mood: {e}")
        logger.exception("📋 Full traceback:")
        try:
            await message.answer("❌ Произошла ошибка.", reply_markup=main_menu_keyboard())
            await state.clear()
        except Exception as inner_e:
            logger.error(f"Failed to send error message in mood handler: {inner_e}")

@router.message(TestFlow.motivation, F.text.in_(["😀 Очень высокая", "🙂 Высокая", "😐 Средняя", "😟 Низкая", "😞 Очень низкая"]))
async def process_motivation(message: types.Message, state: FSMContext):
    """Process motivation response"""
    print("💪 MOTIVATION HANDLER TRIGGERED!")
    print(f"🔍 [MOTIVATION RESPONSE] Raw message: {repr(message.text)}")
    
    try:
        logger.info(f"💪 Processing motivation: {message.text}")
        logger.info(f"🔧 Current state: {await state.get_state()}")
        
        # Save response
        await save_response(message.from_user.id, "Мотивация", message.text)
        logger.info("💾 Motivation response saved to database")
        
        # Set next state and send question
        await state.set_state(TestFlow.problems)
        logger.info(f"✅ New state: {await state.get_state()}")
        
        await message.answer(
            "🤔 Возникли ли у тебя какие-либо проблемы во время рабочего дня?",
            reply_markup=problem_keyboard()
        )
        logger.info("✅ Problems question sent")
        
    except Exception as e:
        logger.error(f"❌ Error in process_motivation: {e}")
        logger.exception("📋 Full traceback:")
        try:
            await message.answer("❌ Произошла ошибка.", reply_markup=main_menu_keyboard())
            await state.clear()
        except Exception as inner_e:
            logger.error(f"Failed to send error message in motivation handler: {inner_e}")

@router.message(TestFlow.problems, F.text.in_(["Да", "Нет"]))
async def process_problems(message: types.Message, state: FSMContext):
    """Process problems response"""
    print("🤔 PROBLEMS HANDLER TRIGGERED!")
    print(f"🔍 [PROBLEMS RESPONSE] Raw message: {repr(message.text)}")
    
    try:
        logger.info(f"🤔 Processing problems: {message.text}")
        logger.info(f"🔧 Current state: {await state.get_state()}")
        
        # Save response
        await save_response(message.from_user.id, "Проблемы", message.text)
        logger.info("💾 Problems response saved to database")
        
        # Send completion and clear state
        await message.answer("🎉 Спасибо за прохождение теста!", reply_markup=main_menu_keyboard())
        await state.clear()
        logger.info("✅ Test flow completed successfully")
        logger.info(f"🧹 Final state: {await state.get_state()}")
        
    except Exception as e:
        logger.error(f"❌ Error in process_problems: {e}")
        logger.exception("📋 Full traceback:")
        try:
            await message.answer("❌ Произошла ошибка.", reply_markup=main_menu_keyboard())
            await state.clear()
        except Exception as inner_e:
            logger.error(f"Failed to send error message in problems handler: {inner_e}")

async def send_daily_test(bot):
    """Send daily test to all users"""
    try:
        users = await get_users()
        logger.info(f"📤 Sending daily test to {len(users)} users")
        
        for user_id in users:
            try:
                await bot.send_message(
                    user_id,
                    "🔔 Пора пройти ежедневный тест",
                    reply_markup=test_keyboard()
                )
                logger.info(f"✅ Daily test sent to user {user_id}")
            except Exception as e:
                logger.error(f"❌ Failed to send daily test to user {user_id}: {e}")
                continue
                
    except Exception as e:
        logger.error(f"❌ Error in send_daily_test: {e}")
        logger.exception("📋 Full traceback:")

print("✅ test_handler.py loaded - Router instance created")
print(f"🔧 Router: {router}")
print(f"🔧 Handlers: {[handler for handler in router.handlers.values()]}")
