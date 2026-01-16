"""
domain/memory.py

But :
- MC : reset mémoire
- MR : injecter la mémoire dans l'expression
- M+ / M- : utilise le dernier résultat
"""

from typing import Tuple
from models.app_state import AppState
from domain.formatting import format_result


def memory_clear(state: AppState) -> AppState:
    state.memory_value = 0.0
    state.message_text = "Mémoire effacée."
    state.message_type = "info"
    return state


def memory_recall(state: AppState) -> Tuple[AppState, str]:
    injected = format_result(state.memory_value)
    state.message_text = "Mémoire rappelée."
    state.message_type = "info"
    return state, injected


def memory_add(state: AppState) -> AppState:
    if state.last_result_value is None:
        state.message_text = "Impossible : aucun résultat à ajouter en mémoire."
        state.message_type = "error"
        state.error_mode = True
        return state

    state.memory_value += state.last_result_value
    state.message_text = "Ajouté à la mémoire."
    state.message_type = "info"
    return state


def memory_sub(state: AppState) -> AppState:
    if state.last_result_value is None:
        state.message_text = "Impossible : aucun résultat à soustraire de la mémoire."
        state.message_type = "error"
        state.error_mode = True
        return state

    state.memory_value -= state.last_result_value
    state.message_text = "Soustrait de la mémoire."
    state.message_type = "info"
    return state
