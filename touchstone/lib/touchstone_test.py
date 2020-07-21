import abc

from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.services.i_service_executor import IServiceExecutor


class TouchstoneTest(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, service_url: str, mocks: Mocks, service_executor: IServiceExecutor):
        self.service_url = service_url
        self.mocks = mocks
        self.service_executor = service_executor

    def processing_period(self) -> float:
        """The amount of time to wait before "then" is executed. This is useful to configure if you are using a mock
        or service that does not operate synchronously (e.g. Rabbit MQ)."""
        return 0.0

    @abc.abstractmethod
    def given(self) -> object:
        """GIVEN this data and/or state. Set the state of the system here."""

    @abc.abstractmethod
    def when(self, given) -> object:
        """WHEN we run this test. Your custom test code goes here. Return the result of the test to be verified."""
        return None

    @abc.abstractmethod
    def then(self, given, result) -> bool:
        """THEN check that the result is correct. Return True/False for a passed/failed test respectively."""
        return False
