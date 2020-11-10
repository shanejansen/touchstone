import abc


class IHealthCheckable(object):
    @abc.abstractmethod
    def is_healthy(self) -> bool:
        pass
