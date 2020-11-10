import abc

from touchstone.lib.health_checks.i_health_checkable import IHealthCheckable
from touchstone.lib.mocks.runnables.i_runnable import IRunnable
from touchstone.lib.networking.i_network import INetwork


class INetworkedRunnable(IRunnable, IHealthCheckable):
    @abc.abstractmethod
    def get_network(self) -> INetwork:
        pass

    @abc.abstractmethod
    def initialize(self):
        pass
