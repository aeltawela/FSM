import unittest
from unittest.mock import MagicMock

from fsm import Fsm, Transition, State

_global_fsm = None


class FsmTest(unittest.TestCase):
    @staticmethod
    def _condition_one():
        return True

    @staticmethod
    def _condition_two():
        return False

    @staticmethod
    def _handler_one():
        pass

    @staticmethod
    def _handler_two():
        global _global_fsm
        _global_fsm.trigger_event("done")

    def test_state_transitions(self):
        fsm = Fsm(
            transitions=(

                Transition(event="done", from_state=State("State 1"), to_state=State("State 2"),
                           condition=self._condition_one,
                           transition_handler=self._handler_one),

                Transition(event="done", from_state=State("State 2"), to_state=State("State 3"),
                           condition=self._condition_one,
                           transition_handler=self._handler_one),
            ),
            initial_state=State("State 1"),
            logger=MagicMock())

        fsm.trigger_event("done")
        self.assertEqual(fsm.current_state, State("State 2"))
        fsm.trigger_event("done")
        self.assertEqual(fsm.current_state, State("State 3"))

    def test_internal_transition(self):
        global _global_fsm

        fsm = Fsm(
            transitions=(
                Transition(event="done", from_state=State("State 1"), to_state=State("State 2"),
                           condition=self._condition_one,
                           transition_handler=self._handler_one),

                Transition(event="done", from_state=State("State 2"), to_state=State("State 3"),
                           condition=self._condition_two,
                           transition_handler=self._handler_one),

                Transition(event="done", from_state=State("State 2"), to_state=State("State 4"),
                           condition=self._condition_one,
                           transition_handler=self._handler_two),

                Transition(event="done", from_state=State("State 4"), to_state=State("State 5"),
                           condition=self._condition_one,
                           transition_handler=self._handler_one),
            ),
            initial_state=State("State 1"),
            logger=MagicMock())

        _global_fsm = fsm

        fsm.trigger_event("done")
        self.assertEqual(fsm.current_state, State("State 2"))
        fsm.trigger_event("done")
        self.assertEqual(fsm.current_state, State("State 5"))


if __name__ == '__main__':
    unittest.main()
