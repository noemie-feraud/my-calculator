import unittest
from models.app_state import create_initial_state
from controller.app_controller import AppController


class DummyUI:
    def render(self, state):
        pass

    def bind_history_clicks(self, controller):
        pass


class TestStateTransitions(unittest.TestCase):
    def test_after_result_digit_resets(self):
        ui = DummyUI()
        st = create_initial_state()
        ctl = AppController(st, ui)

        ctl.handle_digit("1")
        ctl.handle_operator("+")
        ctl.handle_digit("2")
        ctl.handle_equals()

        self.assertTrue(ctl.state.after_result)

        # A digit after a result -> should start a new expression
        ctl.handle_digit("9")
        self.assertEqual(ctl.state.expression_text, "9")


if __name__ == "__main__":
    unittest.main()
