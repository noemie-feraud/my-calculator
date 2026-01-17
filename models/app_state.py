"""
models/app_state.py

Goal:
- Centralize ALL application state in a single object.
- This avoids global variables everywhere.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from models.history_item import HistoryItem


@dataclass
class AppState:
    # Text of the current expression (what the user builds using the buttons)
    expression_text: str = ""

    # Text shown in the display (often the same as expression_text)
    display_text: str = ""

    # Info or error message
    message_text: str = ""
    message_type: str = ""  # "info" / "error" / ""

    # State flags (handy for transitions)
    error_mode: bool = False
    after_result: bool = False
    recall_history: bool = False
    mode_scientifique: bool = False

    # Last computed result
    last_result_value: Optional[float] = None
    last_result_text: str = ""

    # History and memory
    history_items: List[HistoryItem] = field(default_factory=list)
    memory_value: float = 0.0


def create_initial_state() -> AppState:
    """
    Create a consistent initial state
    """
    return AppState()
