import abc

from touchstone.lib.mocks.health_checks.i_health_checkable import IHealthCheckable


class IUrlHealthCheckable(IHealthCheckable):
    @abc.abstractmethod
    def set_url(self, url: str):
        pass
