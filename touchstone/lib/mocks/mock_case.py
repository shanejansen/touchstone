import abc

from touchstone.lib.mocks.mock_context import MockContext


class Setup(object):
    def __init__(self, mock_context: MockContext):
        self.mock_context: MockContext = mock_context

    @abc.abstractmethod
    def load_defaults(self, defaults: dict):
        """Load defaults for this mock provided by the user for dev purposes."""

    @abc.abstractmethod
    def cleanup(self):
        """Return this mock to its original, plain state."""


class Exercise(object):
    def __init__(self, mock_context: MockContext):
        self.mock_context: MockContext = mock_context


class Verify(object):
    def __init__(self, mock_context: MockContext):
        self.mock_context: MockContext = mock_context

    def expected_matches_actual(self, expected, actual):
        if expected == actual:
            return True
        print(f'Expected "{expected}" does not match actual "{actual}".')
        return False
