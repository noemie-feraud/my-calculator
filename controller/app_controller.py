"""
controller/app_controller.py

Goal:

- Receive button clicks
- Apply the "pipeline":
validation -> engine -> formatting -> history/memory -> state update -> UI rendering

- one function per button / action type
- simple helper functions
"""

from models.app_state import AppState, create_initial_state
from models.errors import get_message

from domain.validation import validate_button_action, validate_expression_final
from domain.engine import evaluate_expression
from domain.formatting import format_result
from domain.history import history_add, history_clear, history_select
from domain.memory import memory_clear, memory_recall, memory_add, memory_sub


class AppController:
    def __init__(self, initial_state: AppState, ui) -> None:
        self.state = initial_state
        self.ui = ui
 
    # Helpers (Handy little functions)

    def _render(self) -> None:
        """Display the state in the UI."""
        self.ui.render(self.state)
        # Important: the history is recreated on each render, so we rebind.
        self.ui.bind_history_clicks(self)

    def _set_error(self, code: str) -> None:
        """Set the state to error mode."""
        self.state.message_text = get_message(code)
        self.state.message_type = "error"
        self.state.error_mode = True

    def _set_info(self, text: str) -> None:
        """Set a simple info message."""
        self.state.message_text = text
        self.state.message_type = "info"
        self.state.error_mode = False

    def _clear_message(self) -> None:
        """Delete message."""
        self.state.message_text = ""
        self.state.message_type = ""

    def _clear_entry_keep_history_memory(self) -> None:
        """
        Button C: clears only the expression and the messages.
        Does not touch the history or the memory.
        """

        self.state.expression_text = ""
        self.state.display_text = ""
        self._clear_message()
        self.state.error_mode = False
        self.state.after_result = False
        self.state.recall_history = False

    def _append_token(self, token: str) -> bool:
        """
        Add a token to the expression after validation.
        Return True if OK, False if error.
        """

        ok, err = validate_button_action(self.state.expression_text, token)
        if not ok:
            self._set_error(err or "UNKNOWN_TOKEN")
            return False

        self.state.expression_text += token
        self.state.display_text = self.state.expression_text
        self._clear_message()
        self.state.after_result = False
        self.state.recall_history = False
        return True

    def _append_chars_as_clicks(self, text: str) -> bool:
        """
        To inject a number (e.g., MR), we simulate it "click by click":
        we add each character as if it were a button.
        Example: "-12.5" -> '-', '1', '2', '.', '5'
        """

        for ch in text:
            if ch == "-":
                if not self._append_token("-"):
                    return False
            elif ch.isdigit():
                if not self._append_token(ch):
                    return False
            elif ch == ".":
                if not self._append_token("."):
                    return False
            else:
                # normally we shouldn't have any other characters in MR
                self._set_error("UNKNOWN_TOKEN")
                return False
        return True

    # Button handlers (clicks)

    def handle_digit(self, digit: str) -> None:
        """Buttons 0..9"""
        if self.state.error_mode:
            self._clear_entry_keep_history_memory()

        # If we had a result and we type a digit -> start a new expression
        if self.state.after_result:
            self._clear_entry_keep_history_memory()

        self._append_token(digit)
        self._render()

    def handle_operator(self, op: str) -> None:
        """+ - * / % ^"""
        if self.state.error_mode:
            self._render()
            return

        # After a result: we can continue with "result + ..."
        if self.state.after_result:
            if not self.state.last_result_text:
                self._set_error("NO_LAST_RESULT")
                self._render()
                return
            self.state.expression_text = self.state.last_result_text
            self.state.display_text = self.state.expression_text
            self.state.after_result = False

        self._append_token(op)
        self._render()

    def handle_decimal(self) -> None:
        """Button '.'"""
        if self.state.error_mode:
            self._render()
            return
        self._append_token(".")
        self._render()

    def handle_parenthesis(self, par: str) -> None:
        """Button '(' or ')'"""
        if self.state.error_mode:
            self._render()
            return

        # After a result: if we open a parenthesis, we start over
        if self.state.after_result and par == "(":
            self._clear_entry_keep_history_memory()

        self._append_token(par)
        self._render()

    def handle_scientific_token(self, token: str) -> None:
        """
        Scientific tokens:
        - "sqrt(" "abs(" "inv("
        - "^" "%"
        - "!" postfix
        - "^2" "^3" => we convert into simple clicks: '^' then '2' / '3'
        """
        if self.state.error_mode:
            self._render()
            return

        if token == "^2":
            # Simple and easy to explain: we act as if the user clicks '^' then '2'
            ok1 = self._append_token("^")
            ok2 = self._append_token("2") if ok1 else False
            self._render()
            return

        if token == "^3":
            ok1 = self._append_token("^")
            ok2 = self._append_token("3") if ok1 else False
            self._render()
            return

        # Functions like "sqrt(" etc.: full token (validation handles it)
        self._append_token(token)
        self._render()

    def handle_backspace(self) -> None:
        """Button ⌫"""
        if self.state.error_mode:
            self._clear_entry_keep_history_memory()
            self._render()
            return

        if not self.state.expression_text:
            self._render()
            return

        self.state.expression_text = self.state.expression_text[:-1]
        self.state.display_text = self.state.expression_text
        self._clear_message()
        self._render()

    def handle_clear(self) -> None:
        """Button C: clear the expression."""
        self._clear_entry_keep_history_memory()
        self._render()

    def handle_equals(self) -> None:
        """Button = : final validation, then compute."""
        if self.state.error_mode:
            self._render()
            return

        expr = self.state.expression_text

        ok, err = validate_expression_final(expr)
        if not ok:
            self._set_error(err or "INCOMPLETE_EXPR")
            self._render()
            return

        success, value, engine_err = evaluate_expression(expr)
        if not success or value is None:
            self._set_error(engine_err or "EVAL_ERROR")
            self._render()
            return

        # Display formatting
        result_text = format_result(value)

        # update last_result
        self.state.last_result_value = value
        self.state.last_result_text = result_text

        # Add history
        self.state = history_add(self.state, expr, result_text, value)

        # Display result
        self.state.expression_text = result_text
        self.state.display_text = result_text
        self.state.after_result = True
        self.state.error_mode = False
        self._clear_message()

        self._render()

    def handle_history_click(self, index: int) -> None:
        """Click on a history item."""
        self.state, _ = history_select(self.state, index)
        self._render()

    def handle_history_clear(self) -> None:
        """Delete history"""
        self.state = history_clear(self.state)
        self._render()

    def handle_memory_action(self, action: str) -> None:
        """
        MC / MR / M+ / M-
        """
        if action == "MC":
            self.state = memory_clear(self.state)
            self._render()
            return

        if action == "MR":
            self.state, injected = memory_recall(self.state)

            # We inject the memory as "clicks""
            # Simple rule: if after_result is True, we start a new expression.
            if self.state.after_result:
                self._clear_entry_keep_history_memory()

            ok = self._append_chars_as_clicks(injected)
            if not ok:
                # The error is already set.
                pass

            self._render()
            return

        if action == "M+":
            self.state = memory_add(self.state)
            self._render()
            return

        if action == "M-":
            self.state = memory_sub(self.state)
            self._render()
            return

        # Unknown action.
        self._set_error("UNKNOWN_TOKEN")
        self._render()

    def toggle_scientific_mode(self) -> None:
        """SCI button: show/hide the scientific keypad."""
        self.state.mode_scientifique = not self.state.mode_scientifique
        self._render()

    def handle_reset_all(self) -> None:
        """AC button: full reset (back to the complete initial state)."""
        self.state = create_initial_state()
        self._render()
