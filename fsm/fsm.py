class Transition:
    """
    Transition class which holds only one transition info
    """

    def __init__(self, from_state: str, to_state: str, condition: callable = None, exception_handler: callable = None,
                 retries=None):
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition or self.__true
        self.exception_handler = exception_handler or self.__default_exception_handler
        self.retries = retries or 1

    @staticmethod
    def __true():
        return True

    @staticmethod
    def __default_exception_handler(e: Exception):
        pass


class Fsm:
    """
    The base FSM class
    """

    def __init__(self, transitions: (Transition), initial_state: str, logger=None, console_enabled: bool = None):
        self.transitions = transitions
        self.logger = logger
        self.initial_state = initial_state
        self.console_enabled = console_enabled or True

        if not logger:
            self.logger = None

    def start(self):
        try:
            initial_transition = next((t for t in self.transitions if t.from_state == self.initial_state))
        except StopIteration as e:
            self.logger.error(e)
            self.logger.exception(e)
            raise FsmInitStateException("Can't find the initial state")

        self.__run()

    def __run(self):
        pass

    def __transit(self):
        pass


class FsmInitStateException(Exception):
    pass
