# fsm_states.py
from aiogram.fsm.state import State, StatesGroup

class IdeaFlow(StatesGroup):
    """FSM states for idea submission flow"""
    priority = State()  # User selects priority
    type = State()      # User selects idea type
    description = State()  # User provides description

class ProblemFlow(StatesGroup):
    """FSM states for problem submission flow"""
    severity = State()   # User selects severity
    description = State()  # User provides description
    meeting_needed = State()  # User selects if meeting needed

class TestFlow(StatesGroup):
    """FSM states for daily test flow"""
    mood = State()       # User selects mood
    motivation = State()  # User selects motivation
    problems = State()   # User answers about problems
