# states/test_states.py
from aiogram.fsm.state import State, StatesGroup

class TestFlow(StatesGroup):
    """FSM states for daily test flow"""
    mood = State()          # User selects mood
    motivation = State()    # User selects motivation
    problems = State()      # User answers about problems
