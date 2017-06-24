def _any(*args):
    for arg in args:
        if arg():
            return True

    return False


def any(*args):
    return lambda: _any(*args)


def _all(*args):
    for arg in args:
        if not arg():
            return False

    return True


def all(*args):
    return lambda: _all(*args)


def reverse(condition: callable):
    return lambda: not condition()


class Condition:
    def __init__(self, **kwargs):
        pass
