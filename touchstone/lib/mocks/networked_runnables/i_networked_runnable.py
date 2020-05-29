import abc

from touchstone.lib.mocks.health_checks.i_health_checkable import IHealthCheckable
from touchstone.lib.mocks.network import Network
from touchstone.lib.mocks.runnables.i_runnable import IRunnable


class INetworkedRunnable(IRunnable, IHealthCheckable):
    @abc.abstractmethod
    def get_network(self) -> Network:
        pass

    @abc.abstractmethod
    def initialize(self):
        pass
