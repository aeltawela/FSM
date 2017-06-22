from .state import State


class Transition:
    """
    Transition class which holds only one transition info
    """

    def __init__(self, event: str, from_state: State, to_state: State, condition: callable = None,
                 transition_handler: callable = None,
                 exception_state: State = None,
                 retries=None):
        self.event = event
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition or (lambda: True)
        self.transition_handler = transition_handler or (lambda: None)
        self.exception_state = exception_state
        self.retries = retries or 1
