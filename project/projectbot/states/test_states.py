# states/test_states.py
from aiogram.fsm.state import State, StatesGroup


class TestFlow(StatesGroup):
    """FSM states for daily test flow"""
    mood = State()                    # User selects mood
    motivation = State()              # User selects motivation
    problems = State()                # User answers about problems (Да/Нет)
    problem_severity = State()        # User selects problem severity (only if Да)
    problem_description = State()     # User describes the problem
    problem_meeting = State()         # User answers if meeting is needed
