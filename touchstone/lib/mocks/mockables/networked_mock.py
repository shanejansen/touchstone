from touchstone.lib import exceptions
from touchstone.lib.health_checks.i_health_checkable import IHealthCheckable
from touchstone.lib.mocks.mockables.i_mockable import IMockable
from touchstone.lib.mocks.networked_runnables.i_networked_runnable import INetworkedRunnable
from touchstone.lib.mocks.runnables.i_runnable import IRunnable
from touchstone.lib.networking.i_network import INetwork


class NetworkedMock(IMockable, IHealthCheckable):
    def __init__(self, name: str, pretty_name: str, networked_runnable: INetworkedRunnable):
        self.__name = name
        self.__pretty_name = pretty_name
        self.__networked_runnable = networked_runnable
        self.__has_initialized = False

    def get_name(self):
        return self.__name

    def get_pretty_name(self):
        return self.__pretty_name

    def get_runnable(self) -> IRunnable:
        return self.__networked_runnable

    def start(self):
        self.__networked_runnable.start()

    def stop(self):
        self.__networked_runnable.stop()

    def reset(self):
        self.__networked_runnable.reset()

    def services_available(self):
        self.__networked_runnable.services_available()

    def is_healthy(self) -> bool:
        try:
            self.__networked_runnable.get_network()
        except exceptions.MockException:
            return False
        is_healthy = self.__networked_runnable.is_healthy()
        if is_healthy and not self.__has_initialized:
            self.__networked_runnable.initialize()
            self.__has_initialized = True
        return is_healthy

    def get_network(self) -> INetwork:
        return self.__networked_runnable.get_network()
