"""
ui/app_view.py

But :
- Construire l'interface CustomTkinter
- Aucun calcul ici
- Clic uniquement (pas de saisie clavier PC)
- Display non éditable : on utilise un Label
"""

import customtkinter as ctk
from typing import List
from models.app_state import AppState
from models.history_item import HistoryItem


class AppView:
    def __init__(self) -> None:
        # Setup customtkinter
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Pascaline - Calculatrice")
        self.window.geometry("900x520")

        # Layout principal : gauche = calculatrice, droite = historique
        self.left_frame = ctk.CTkFrame(self.window)
        self.right_frame = ctk.CTkFrame(self.window)

        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.window.grid_columnconfigure(0, weight=3)
        self.window.grid_columnconfigure(1, weight=2)
        self.window.grid_rowconfigure(0, weight=1)

        # Display (label, pas éditable)
        self.display_label = ctk.CTkLabel(
            self.left_frame,
            text="",
            font=("Consolas", 28),
            anchor="e"  # align à droite
        )
        self.display_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 2))

        # Zone message (erreurs/infos)
        self.message_label = ctk.CTkLabel(
            self.left_frame,
            text="",
            font=("Arial", 14),
            anchor="w"
        )
        self.message_label.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.left_frame.grid_columnconfigure(0, weight=1)

        # Zone boutons
        self.keyboard_frame = ctk.CTkFrame(self.left_frame)
        self.keyboard_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.grid_rowconfigure(2, weight=1)

        # Frames standard vs scientifique
        self.standard_frame = ctk.CTkFrame(self.keyboard_frame)
        self.scientific_frame = ctk.CTkFrame(self.keyboard_frame)

        self.standard_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.scientific_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.keyboard_frame.grid_columnconfigure(0, weight=3)
        self.keyboard_frame.grid_columnconfigure(1, weight=2)
        self.keyboard_frame.grid_rowconfigure(0, weight=1)

        # Historique (droite)
        self.history_title = ctk.CTkLabel(self.right_frame, text="Historique", font=("Arial", 18))
        self.history_title.pack(pady=(10, 5))

        self.history_scroll = ctk.CTkScrollableFrame(self.right_frame, width=320, height=350)
        self.history_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.history_buttons_frame = ctk.CTkFrame(self.right_frame)
        self.history_buttons_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_clear_history = ctk.CTkButton(self.history_buttons_frame, text="Effacer historique")
        self.btn_reset_all = ctk.CTkButton(self.history_buttons_frame, text="Réinitialiser (AC)")
        self.btn_clear_history.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.btn_reset_all.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.history_buttons_frame.grid_columnconfigure(0, weight=1)
        self.history_buttons_frame.grid_columnconfigure(1, weight=1)

        # On stocke les boutons pour les brancher facilement
        self.btns_digit = {}
        self.btns_op = {}
        self.btn_decimal = None
        self.btn_open_par = None
        self.btn_close_par = None
        self.btn_backspace = None
        self.btn_clear = None
        self.btn_equals = None
        self.btn_sci_toggle = None

        self.btns_sci = {}  # token -> button
        self.btns_mem = {}  # action -> button

        # Boutons d'historique recréés à chaque render
        self._history_row_buttons: List[ctk.CTkButton] = []

        # Construction
        self._build_standard_buttons()
        self._build_scientific_buttons()

    def mainloop(self) -> None:
        self.window.mainloop()

    # -------------------------
    # Construction boutons
    # -------------------------

    def _build_standard_buttons(self) -> None:
        """
        Crée les boutons standard.
        """
        grid = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["(", ")", "C", "⌫"],
        ]

        for r, row in enumerate(grid):
            for c, label in enumerate(row):
                btn = ctk.CTkButton(self.standard_frame, text=label, width=70, height=45)
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                self.standard_frame.grid_columnconfigure(c, weight=1)

                if label.isdigit():
                    self.btns_digit[label] = btn
                elif label in {"+", "-", "*", "/"}:
                    self.btns_op[label] = btn
                elif label == ".":
                    self.btn_decimal = btn
                elif label == "(":
                    self.btn_open_par = btn
                elif label == ")":
                    self.btn_close_par = btn
                elif label == "C":
                    self.btn_clear = btn
                elif label == "⌫":
                    self.btn_backspace = btn
                elif label == "=":
                    self.btn_equals = btn

        # Bouton SCI (toggle)
        self.btn_sci_toggle = ctk.CTkButton(self.standard_frame, text="SCI", width=70, height=45)
        self.btn_sci_toggle.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    def _build_scientific_buttons(self) -> None:
        """
        Crée les boutons scientifiques.
        On envoie des tokens au controller.
        """
        sci_buttons = [
            ("√", "sqrt("),
            ("|x|", "abs("),
            ("1/x", "inv("),
            ("^", "^"),
            ("x²", "^2"),
            ("x³", "^3"),
            ("%", "%"),
            ("!", "!"),
        ]

        idx = 0
        for r in range(4):
            for c in range(2):
                label, token = sci_buttons[idx]
                idx += 1
                btn = ctk.CTkButton(self.scientific_frame, text=label, width=90, height=45)
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                self.scientific_frame.grid_columnconfigure(c, weight=1)
                self.btns_sci[token] = btn

        # Mémoire : MC MR M+ M-
        mem = [("MC", "MC"), ("MR", "MR"), ("M+", "M+"), ("M-", "M-")]
        start_row = 4
        idx = 0
        for r in range(2):
            for c in range(2):
                label, action = mem[idx]
                idx += 1
                btn = ctk.CTkButton(self.scientific_frame, text=label, width=90, height=40)
                btn.grid(row=start_row + r, column=c, padx=5, pady=5, sticky="nsew")
                self.btns_mem[action] = btn

    # -------------------------
    # Binding boutons
    # -------------------------

    def bind_buttons(self, controller) -> None:
        """
        Branche les boutons sur le controller.
        AUCUN clavier PC : uniquement des clicks.
        """
        for digit, btn in self.btns_digit.items():
            btn.configure(command=lambda d=digit: controller.handle_digit(d))

        for op, btn in self.btns_op.items():
            btn.configure(command=lambda o=op: controller.handle_operator(o))

        if self.btn_decimal:
            self.btn_decimal.configure(command=lambda: controller.handle_decimal())
        if self.btn_open_par:
            self.btn_open_par.configure(command=lambda: controller.handle_parenthesis("("))
        if self.btn_close_par:
            self.btn_close_par.configure(command=lambda: controller.handle_parenthesis(")"))

        if self.btn_backspace:
            self.btn_backspace.configure(command=lambda: controller.handle_backspace())
        if self.btn_clear:
            self.btn_clear.configure(command=lambda: controller.handle_clear())
        if self.btn_equals:
            self.btn_equals.configure(command=lambda: controller.handle_equals())

        if self.btn_sci_toggle:
            self.btn_sci_toggle.configure(command=lambda: controller.toggle_scientific_mode())

        # Scientifique tokens
        for token, btn in self.btns_sci.items():
            btn.configure(command=lambda t=token: controller.handle_scientific_token(t))

        # Mémoire
        for action, btn in self.btns_mem.items():
            btn.configure(command=lambda a=action: controller.handle_memory_action(a))

        # Historique actions
        self.btn_clear_history.configure(command=lambda: controller.handle_history_clear())
        self.btn_reset_all.configure(command=lambda: controller.handle_reset_all())

    def bind_history_clicks(self, controller) -> None:
        """
        Branche les boutons d'historique.
        On doit le refaire après chaque render car la liste est recréée.
        """
        for i, btn in enumerate(self._history_row_buttons):
            btn.configure(command=lambda idx=i: controller.handle_history_click(idx))

    # -------------------------
    # Render
    # -------------------------

    def render(self, state: AppState) -> None:
        """
        Met à jour :
        - display
        - message
        - visibilité du clavier scientifique
        - historique
        """
        self.display_label.configure(text=state.display_text)

        # Message : couleur simple (facile à expliquer)
        if state.message_type == "error":
            self.message_label.configure(text=state.message_text, text_color="red")
        elif state.message_type == "info":
            self.message_label.configure(text=state.message_text, text_color="green")
        else:
            self.message_label.configure(text="", text_color="gray")

        # Afficher/masquer scientifique
        if state.mode_scientifique:
            self.scientific_frame.grid()
        else:
            self.scientific_frame.grid_remove()

        # Historique
        self._render_history(state.history_items)

    def _render_history(self, items: List[HistoryItem]) -> None:
        """
        Recrée complètement la liste d'historique.
        C'est simple mais efficace.
        """
        # détruire anciens boutons
        for btn in self._history_row_buttons:
            btn.destroy()
        self._history_row_buttons = []

        for item in items:
            text = f"{item.expr} = {item.result_text}"
            btn = ctk.CTkButton(self.history_scroll, text=text, anchor="w")
            btn.pack(fill="x", padx=5, pady=3)
            self._history_row_buttons.append(btn)
