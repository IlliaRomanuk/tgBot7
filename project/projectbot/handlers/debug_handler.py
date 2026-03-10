# handlers/debug_handler.py - Separate debug router
import logging
from aiogram import Router, types

logger = logging.getLogger(__name__)
router = Router()

@router.message()
async def global_debug_handler(message: types.Message):
    """Global debug handler - Catches ONLY truly unhandled messages"""
    print("🚨 GLOBAL DEBUG HANDLER TRIGGERED!")
    print(f"🔍 [GLOBAL DEBUG] Raw message: {repr(message.text)}")
    print(f"🔍 [GLOBAL DEBUG] Lowercase: {repr(message.text.lower())}")
    print(f"🔍 [GLOBAL DEBUG] Type: {type(message.text)}")
    print(f"🔍 [GLOBAL DEBUG] Length: {len(message.text) if message.text else 'None'}")
    
    logger.warning(f"🚨 UNHANDLED MESSAGE: '{message.text}' from user {message.from_user.id}")
    logger.warning(f"🚨 No specific handler matched this message")
    
    try:
        await message.reply(
            f"🔍 Debug: Received '{message.text}'\n"
            f"❌ No matching handler found\n"
            f"💡 Try: /start, /help, or use menu buttons"
        )
        logger.info("✅ Global debug reply sent")
    except Exception as e:
        logger.error(f"❌ Failed to send debug reply: {e}")

print("✅ debug_handler.py loaded - Router instance created")
print(f"🔧 Router: {router}")
print(f"🔧 Handlers: {[handler for handler in router.handlers.values()]}")
