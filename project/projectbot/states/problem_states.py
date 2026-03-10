# states/problem_states.py
from aiogram.fsm.state import State, StatesGroup

class ProblemFlow(StatesGroup):
    """FSM states for problem submission flow"""
    severity = State()      # User selects severity
    description = State()  # User provides description
    meeting_needed = State()  # User selects if meeting needed
