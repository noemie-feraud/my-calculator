"""
models/history_item.py

But :
- Une ligne d'historique doit avoir :
  - l'expression
  - le résultat affichable
  - la valeur numérique réelle (float)
"""

from dataclasses import dataclass


@dataclass
class HistoryItem:
    expr: str
    result_text: str
    result_value: float


def create_history_item(expr: str, result_text: str, result_value: float) -> HistoryItem:
    """Crée une entrée d'historique."""
    return HistoryItem(expr=expr, result_text=result_text, result_value=result_value)
