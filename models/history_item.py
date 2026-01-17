"""
models/history_item.py

Goal:
- A history line must have:
  - the expression
  - the displayable result
  - the real numeric value (float)
"""

from dataclasses import dataclass


@dataclass
class HistoryItem:
    expr: str
    result_text: str
    result_value: float


def create_history_item(expr: str, result_text: str, result_value: float) -> HistoryItem:
    """Create a history entry"""
    return HistoryItem(expr=expr, result_text=result_text, result_value=result_value)
