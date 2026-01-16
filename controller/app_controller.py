"""
controller/app_controller.py

But :
- Recevoir les clics des boutons
- Appliquer le "pipeline" :
  validation -> moteur -> formatage -> historique/mémoire -> mise à jour état -> rendu UI

- une fonction par bouton / type d'action
- des helpers simples
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

    # ----------------------
    # Helpers (petites fonctions pratiques)
    # ----------------------

    def _render(self) -> None:
        """Affiche l'état dans l'UI."""
        self.ui.render(self.state)
        # Important : l'historique est recréé à chaque render, donc on rebinde
        self.ui.bind_history_clicks(self)

    def _set_error(self, code: str) -> None:
        """Met l'état en mode erreur."""
        self.state.message_text = get_message(code)
        self.state.message_type = "error"
        self.state.error_mode = True

    def _set_info(self, text: str) -> None:
        """Met un message d'info simple."""
        self.state.message_text = text
        self.state.message_type = "info"
        self.state.error_mode = False

    def _clear_message(self) -> None:
        """Efface message."""
        self.state.message_text = ""
        self.state.message_type = ""

    def _clear_entry_keep_history_memory(self) -> None:
        """
        Bouton C : efface juste l'expression et les messages.
        Ne touche pas à l'historique ni à la mémoire.
        """
        self.state.expression_text = ""
        self.state.display_text = ""
        self._clear_message()
        self.state.error_mode = False
        self.state.after_result = False
        self.state.recall_history = False

    def _append_token(self, token: str) -> bool:
        """
        Ajoute un token à l'expression après validation.
        Retourne True si OK, False si erreur.
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
        Pour injecter un nombre (ex: MR) on simule "clic par clic" :
        on ajoute chaque caractère comme si c'était un bouton.
        Exemple : "-12.5" -> '-', '1', '2', '.', '5'
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
                # normalement on ne doit pas avoir d'autres caractères dans MR
                self._set_error("UNKNOWN_TOKEN")
                return False
        return True

    # ----------------------
    # Handlers boutons (clics)
    # ----------------------

    def handle_digit(self, digit: str) -> None:
        """Boutons 0..9"""
        if self.state.error_mode:
            self._clear_entry_keep_history_memory()

        # si on avait un résultat et on tape un chiffre -> nouvelle expression
        if self.state.after_result:
            self._clear_entry_keep_history_memory()

        self._append_token(digit)
        self._render()

    def handle_operator(self, op: str) -> None:
        """+ - * / % ^"""
        if self.state.error_mode:
            self._render()
            return

        # après résultat : on peut enchaîner "résultat + ..."
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
        """Bouton '.'"""
        if self.state.error_mode:
            self._render()
            return
        self._append_token(".")
        self._render()

    def handle_parenthesis(self, par: str) -> None:
        """Bouton '(' ou ')'"""
        if self.state.error_mode:
            self._render()
            return

        # après résultat : si on ouvre une parenthèse, on recommence
        if self.state.after_result and par == "(":
            self._clear_entry_keep_history_memory()

        self._append_token(par)
        self._render()

    def handle_scientific_token(self, token: str) -> None:
        """
        Tokens scientifiques :
        - "sqrt(" "abs(" "inv("
        - "^" "%"
        - "!" postfix
        - "^2" "^3" => on transforme en clics simples : '^' puis '2' / '3'
        """
        if self.state.error_mode:
            self._render()
            return

        if token == "^2":
            # simple et explicable : on fait comme si l'utilisateur clique '^' puis '2'
            ok1 = self._append_token("^")
            ok2 = self._append_token("2") if ok1 else False
            self._render()
            return

        if token == "^3":
            ok1 = self._append_token("^")
            ok2 = self._append_token("3") if ok1 else False
            self._render()
            return

        # fonctions "sqrt(" etc : token complet (validation le gère)
        self._append_token(token)
        self._render()

    def handle_backspace(self) -> None:
        """Bouton ⌫"""
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
        """Bouton C : effacer l'expression"""
        self._clear_entry_keep_history_memory()
        self._render()

    def handle_equals(self) -> None:
        """Bouton = : validation finale puis calcul"""
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

        # formatage affichage
        result_text = format_result(value)

        # mise à jour last_result
        self.state.last_result_value = value
        self.state.last_result_text = result_text

        # ajout historique
        self.state = history_add(self.state, expr, result_text, value)

        # affichage du résultat
        self.state.expression_text = result_text
        self.state.display_text = result_text
        self.state.after_result = True
        self.state.error_mode = False
        self._clear_message()

        self._render()

    def handle_history_click(self, index: int) -> None:
        """Clique sur un élément d'historique"""
        self.state, _ = history_select(self.state, index)
        self._render()

    def handle_history_clear(self) -> None:
        """Effacer historique"""
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

            # On injecte la mémoire comme des "clics"
            # Règle simple : si after_result True, on recommence une expression
            if self.state.after_result:
                self._clear_entry_keep_history_memory()

            ok = self._append_chars_as_clicks(injected)
            if not ok:
                # l'erreur est déjà posée
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

        # action inconnue
        self._set_error("UNKNOWN_TOKEN")
        self._render()

    def toggle_scientific_mode(self) -> None:
        """Bouton SCI : afficher/masquer le clavier scientifique"""
        self.state.mode_scientifique = not self.state.mode_scientifique
        self._render()

    def handle_reset_all(self) -> None:
        """Bouton AC : reset total (état initial complet)"""
        self.state = create_initial_state()
        self._render()
