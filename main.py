"""
main.py
Point d'entrée de l'application.

Ici on ne fait PAS de calcul.
On crée :
- l'état initial
- l'UI
- le controller
Puis on branche les boutons et on lance la fenêtre.
"""

from models.app_state import create_initial_state
from ui.app_view import AppView
from controller.app_controller import AppController


def main() -> None:
    """Démarre l'app."""
    state = create_initial_state()

    ui = AppView()
    controller = AppController(initial_state=state, ui=ui)

    # On branche UNIQUEMENT les boutons (clics), pas le clavier du PC
    ui.bind_buttons(controller)

    # Premier affichage
    ui.render(controller.state)
    ui.bind_history_clicks(controller)  # l'historique est vide au début, mais on garde la logique

    # Boucle principale (fenêtre)
    ui.mainloop()


if __name__ == "__main__":
    main()
