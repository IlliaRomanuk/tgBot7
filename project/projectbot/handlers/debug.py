"""Debug handler - catches unhandled messages."""
import logging
from aiogram import Router, types

logger = logging.getLogger(__name__)
router = Router()


@router.message()
async def debug_handler(message: types.Message) -> None:
    """Handle unhandled messages for debugging.
    
    This handler MUST be registered last and acts as a catch-all
    for any messages that didn't match other handlers.
    """
    logger.warning(
        f"🚨 DEBUG HANDLER TRIGGERED - Unhandled message: '{message.text}' "
        f"from user {message.from_user.id}"
    )
    
    await message.answer(
        f"🔍 <b>Debug Info</b>\n\n"
        f"Received: <code>{message.text}</code>\n"
        f"No handler matched this message.\n\n"
        f"Use /start to see available options."
    )
