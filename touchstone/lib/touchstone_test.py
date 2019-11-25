import abc

from touchstone.lib.mocks.mocks import Mocks


class TouchstoneTest(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, mocks: Mocks):
        self.mocks = mocks

    @abc.abstractmethod
    def given(self):
        """GIVEN this data and/or state. Set the state of the system here."""

    @abc.abstractmethod
    def when(self):
        """WHEN we run this test. Your custom test code goes here. Return the result of the test to be verified."""
        return None

    @abc.abstractmethod
    def then(self, test_result) -> bool:
        """THEN check that the result is correct. Return True/False for a passed/failed test respectively."""
        return False
