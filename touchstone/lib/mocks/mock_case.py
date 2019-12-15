import abc


class Setup(object):
    @abc.abstractmethod
    def load_defaults(self, defaults: dict):
        """Loads defaults for this mock provided by the user for dev purposes."""

    @abc.abstractmethod
    def reset(self):
        """Returns this mock to its original state."""


class Exercise(object):
    pass


class Verify(object):
    def expected_matches_actual(self, expected, actual):
        if expected == actual:
            return True
        print(f'Expected "{expected}" does not match actual "{actual}".')
        return False
