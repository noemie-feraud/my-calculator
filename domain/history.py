"""
domain/history.py

But :
- Gérer l'historique en mémoire (liste).
- Pas de base de données.
"""

from typing import Tuple
from models.app_state import AppState
from models.history_item import create_history_item


def history_add(state: AppState, expr: str, result_text: str, result_value: float) -> AppState:
    item = create_history_item(expr, result_text, result_value)
    state.history_items.append(item)
    return state


def history_clear(state: AppState) -> AppState:
    state.history_items = []
    return state


def history_select(state: AppState, index: int) -> Tuple[AppState, str]:
    if index < 0 or index >= len(state.history_items):
        state.message_text = "Élément d'historique introuvable."
        state.message_type = "error"
        state.error_mode = True
        return state, ""

    expr = state.history_items[index].expr
    state.expression_text = expr
    state.display_text = expr

    state.message_text = ""
    state.message_type = ""
    state.error_mode = False
    state.after_result = False
    state.recall_history = True
    return state, expr
