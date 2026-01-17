"""
domain/memory.py

Goal:
- MC: reset memory
- MR: inject memory into the expression
- M+ / M-: use the last result
"""

from typing import Tuple
from models.app_state import AppState
from domain.formatting import format_result


def memory_clear(state: AppState) -> AppState:
    state.memory_value = 0.0
    state.message_text = "Memory cleared"
    state.message_type = "info"
    return state


def memory_recall(state: AppState) -> Tuple[AppState, str]:
    injected = format_result(state.memory_value)
    state.message_text = "Memory recalled"
    state.message_type = "info"
    return state, injected


def memory_add(state: AppState) -> AppState:
    if state.last_result_value is None:
        state.message_text = "Impossible: no result to add to memory"
        state.message_type = "error"
        state.error_mode = True
        return state

    state.memory_value += state.last_result_value
    state.message_text = "Added to memory"
    state.message_type = "info"
    return state


def memory_sub(state: AppState) -> AppState:
    if state.last_result_value is None:
        state.message_text = "Impossible: no result to subtract from memory"
        state.message_type = "error"
        state.error_mode = True
        return state

    state.memory_value -= state.last_result_value
    state.message_text = "Subtracted from memory"
    state.message_type = "info"
    return state
