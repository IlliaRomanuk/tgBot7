"""Handlers package initialization - exports all routers."""
from .start import router as start_router
from .test import router as test_router
from .idea import router as idea_router
from .problem import router as problem_router
from .debug import router as debug_router

__all__ = [
    "start_router",
    "test_router", 
    "idea_router",
    "problem_router",
    "debug_router"
]
