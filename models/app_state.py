"""
models/app_state.py

But :
- Centraliser TOUT l'état de l'application dans un seul objet.
- Ça évite les variables globales partout.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from models.history_item import HistoryItem


@dataclass
class AppState:
    # Texte de l'expression en cours (ce que l'utilisateur construit via les boutons)
    expression_text: str = ""

    # Texte affiché dans le display (souvent pareil que expression_text)
    display_text: str = ""

    # Message d'info ou d'erreur
    message_text: str = ""
    message_type: str = ""  # "info" / "error" / ""

    # Flags d'état (pratique pour les transitions)
    error_mode: bool = False
    after_result: bool = False
    recall_history: bool = False
    mode_scientifique: bool = False

    # Dernier résultat calculé
    last_result_value: Optional[float] = None
    last_result_text: str = ""

    # Historique et mémoire
    history_items: List[HistoryItem] = field(default_factory=list)
    memory_value: float = 0.0


def create_initial_state() -> AppState:
    """
    Crée un état initial cohérent.
    """
    return AppState()
