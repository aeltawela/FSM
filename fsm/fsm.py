from .state import State
from .transition import Transition


class Fsm:
    """
    The base FSM class
    """

    def __init__(self, transitions: (Transition) = None, initial_state: State = None, logger=None,
                 console_enabled: bool = None):

        if transitions:
            self.__init_transitions(transitions)

        self.current_state = initial_state
        self.__machine_running = False
        self.console_enabled = console_enabled or True

        self.__event_queue = list()
        self.__init_logger(logger)

    def __init_transitions(self, transitions):
        self.transitions = dict()

        for transition in transitions:
            self.transitions.setdefault(transition.from_state, dict()).setdefault(transition.event, []).append(
                transition)

    def __init_logger(self, logger):
        self.logger = logger

    def trigger_event(self, name: str):
        """
        Trigger event
        :param name: event name
        :return: void
        """

        possible_transitions = self.transitions.get(self.current_state, dict()).get(name)

        if not possible_transitions:
            raise FsmEventNotExist(name, "Event doesn't exists")

        for transition in possible_transitions:
            if transition.condition():
                self.__event_queue.append(transition)
                break

        if not self.__machine_running:
            self.__transit()

    def __transit(self):
        try:
            self.__machine_running = True
            while self.__event_queue:

                transition = self.__event_queue.pop()
                self.logger.info("Transiting from {} to {}".format(transition.from_state, transition.to_state))

                for retry in range(transition.retries):
                    try:
                        self.logger.info("retry no.: {}".format(retry))
                        transition.from_state.on_exist()
                        transition.transition_handler()
                        transition.to_state.on_enter()
                        self.current_state = transition.to_state
                        break
                    except Exception as e:
                        self.logger.exception(e)

        finally:
            self.__machine_running = False


class FsmInitStateException(Exception):
    pass


class FsmEventNotExist(Exception):
    def __init__(self, event, *args):
        self.event = event
        super().__init__(*args)

    def __str__(self):
        return "Event: {} msg: {}".format(self.event, super(FsmEventNotExist, self).__str__())
