import abc

from test_context import TestContext


class TouchstoneTest(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def name(self) -> str:
        """A name for this Touchstone test."""

    @abc.abstractmethod
    def given(self, test_context: TestContext):
        """GIVEN this data and/or state. Set the state of the system here."""

    @abc.abstractmethod
    def when(self, test_context: TestContext):
        """WHEN we run this test. Your custom test code goes here. Return the result of the test to be verified."""
        return None

    @abc.abstractmethod
    def then(self, test_context: TestContext, test_result) -> bool:
        """THEN check that the result is correct. Return True/False for a passed/failed test respectively."""
        return False
