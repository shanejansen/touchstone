import abc

from touchstone.lib.mocks.networked_runnables.http.http_setup import HttpSetup
from touchstone.lib.mocks.networked_runnables.http.http_verify import HttpVerify


class IHttpBehavior(object):
    @abc.abstractmethod
    def setup(self) -> HttpSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> HttpVerify:
        pass

    @abc.abstractmethod
    def url(self) -> str:
        pass
