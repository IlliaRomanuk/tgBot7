# states/idea_states.py
from aiogram.fsm.state import State, StatesGroup

class IdeaFlow(StatesGroup):
    """FSM states for idea submission flow"""
    priority = State()     # User selects priority
    idea_type = State()    # User selects idea type
    description = State()  # User provides description
