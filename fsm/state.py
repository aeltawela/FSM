class State:
    """
    Class which hold state name and on_enter/on_exist callables
    """

    def __init__(self, name: str, on_enter: callable = None, on_exist: callable = None):
        self.name = name
        self.on_enter = on_enter or (lambda: None)
        self.on_exist = on_exist or (lambda: None)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return repr(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)
