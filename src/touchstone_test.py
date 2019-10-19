import abc


class TouchstoneTest(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def name(self):
        """A name for this Touchstone test."""
        return 'Undefined'

    @abc.abstractmethod
    def given(self, given_context):
        """GIVEN this data and/or state. Set the state of the system here."""

    @abc.abstractmethod
    def when(self, when_context):
        """WHEN we run this test. Your custom test code goes here. Return the result of the test to be verified."""
        return None

    @abc.abstractmethod
    def then(self, then_context, test_result):
        """THEN check that the result is correct. Return True/False for a passed/failed test respectively."""
        return False
