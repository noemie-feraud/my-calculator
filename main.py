"""
main.py
Application entry point.

We do NOT perform any calculations here.
We create:
- the initial state
- the UI
- the controller
Then we bind the buttons and launch the window.
"""

from models.app_state import create_initial_state
from ui.app_view import AppView
from controller.app_controller import AppController


def main() -> None:
    """Start the app"""
    state = create_initial_state()

    ui = AppView()
    controller = AppController(initial_state=state, ui=ui)

    # We bind ONLY the buttons (clicks), not the PC keyboard
    ui.bind_buttons(controller)

    # First display
    ui.render(controller.state)
    ui.bind_history_clicks(controller)  # The history is empty at the beginning, but we keep the logic

    # Main loop (window)
    ui.mainloop()


if __name__ == "__main__":
    main()
