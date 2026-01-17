"""
ui/app_view.py

Goal:
- Build the CustomTkinter interface
- No calculations here
- Clicks only (no PC keyboard input)
- Non-editable display: we use a Label
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

        # Global scaling (larger UI)
        ctk.set_widget_scaling(2.0)   # Widget sizes (buttons, labels, etc.)
        ctk.set_window_scaling(1.9)   # Global window scaling


        self.window = ctk.CTk()
        self.window.title("Pascaline - Calculatrice")
        self.window.geometry("900x520")

        # Main layout: left = calculator, right = history
        self.left_frame = ctk.CTkFrame(self.window)
        self.right_frame = ctk.CTkFrame(self.window)

        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.window.grid_columnconfigure(0, weight=3)
        self.window.grid_columnconfigure(1, weight=2)
        self.window.grid_rowconfigure(0, weight=1)

        # Display (label, non-editable)
        self.display_label = ctk.CTkLabel(
            self.left_frame,
            text="",
            font=("Consolas", 28),
            anchor="e"  # Right-aligned
        )
        self.display_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 2))

        # Message area (errors/info)
        self.message_label = ctk.CTkLabel(
            self.left_frame,
            text="",
            font=("Arial", 14),
            anchor="w"
        )
        self.message_label.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.left_frame.grid_columnconfigure(0, weight=1)

        # Buttons area
        self.keyboard_frame = ctk.CTkFrame(self.left_frame)
        self.keyboard_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.grid_rowconfigure(2, weight=1)

        # Frames standard vs scientific
        self.standard_frame = ctk.CTkFrame(self.keyboard_frame)
        self.scientific_frame = ctk.CTkFrame(self.keyboard_frame)

        self.standard_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.scientific_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.keyboard_frame.grid_columnconfigure(0, weight=3)
        self.keyboard_frame.grid_columnconfigure(1, weight=2)
        self.keyboard_frame.grid_rowconfigure(0, weight=1)

        # History (right)
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

        # We store the buttons so we can wire them up easily
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

        # History buttons are recreated on each render
        self._history_row_buttons: List[ctk.CTkButton] = []

        # Construction
        self._build_standard_buttons()
        self._build_scientific_buttons()

    def mainloop(self) -> None:
        self.window.mainloop()


    # Buttons construction

    def _build_standard_buttons(self) -> None:
        """
        Create the standard buttons
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
                    self.btn_equals.configure(fg_color="dark green", hover_color="#345c3e")

        # SCI button (toggle)
        self.btn_sci_toggle = ctk.CTkButton(self.standard_frame, text="SCI", width=70, height=45)
        self.btn_sci_toggle.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    def _build_scientific_buttons(self) -> None:
        """
        Create the scientific buttons.
        We send tokens to the controller.
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

        # Memory : MC MR M+ M-
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


    # Buttons binding

    def bind_buttons(self, controller) -> None:
        """
        Bind the buttons to the controller.
        NO PC keyboard: clicks only.
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

        # Scientific tokens
        for token, btn in self.btns_sci.items():
            btn.configure(command=lambda t=token: controller.handle_scientific_token(t))

        # Memory
        for action, btn in self.btns_mem.items():
            btn.configure(command=lambda a=action: controller.handle_memory_action(a))

        # History actions
        self.btn_clear_history.configure(command=lambda: controller.handle_history_clear())
        self.btn_reset_all.configure(command=lambda: controller.handle_reset_all())

    def bind_history_clicks(self, controller) -> None:
        """
        Bind the history buttons.
        We must redo it after each render because the list is recreated.
        """
        for i, btn in enumerate(self._history_row_buttons):
            btn.configure(command=lambda idx=i: controller.handle_history_click(idx))


    # Render

    def render(self, state: AppState) -> None:
        """
        Update:
        - display
        - message
        - scientific keypad visibility
        - history
        """
        self.display_label.configure(text=state.display_text)

        # Message : simple color 
        if state.message_type == "error":
            self.message_label.configure(text=state.message_text, text_color="red")
        elif state.message_type == "info":
            self.message_label.configure(text=state.message_text, text_color="green")
        else:
            self.message_label.configure(text="", text_color="gray")

        # Show/hide scientific
        if state.mode_scientifique:
            self.scientific_frame.grid()
        else:
            self.scientific_frame.grid_remove()

        # History
        self._render_history(state.history_items)

    def _render_history(self, items: List[HistoryItem]) -> None:
        """
        Fully recreate the history list.
        It's simple but effective.
        """
        # Destroy old buttons
        for btn in self._history_row_buttons:
            btn.destroy()
        self._history_row_buttons = []

        for item in items:
            text = f"{item.expr} = {item.result_text}"
            btn = ctk.CTkButton(self.history_scroll, text=text, anchor="w")
            btn.pack(fill="x", padx=5, pady=3)
            self._history_row_buttons.append(btn)
