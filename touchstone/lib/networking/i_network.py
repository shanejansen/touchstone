import abc


class INetwork(object):
    @abc.abstractmethod
    def internal_host(self) -> str:
        pass

    @abc.abstractmethod
    def external_host(self) -> str:
        pass

    @abc.abstractmethod
    def internal_port(self) -> int:
        pass

    @abc.abstractmethod
    def external_port(self) -> int:
        pass

    @abc.abstractmethod
    def username(self) -> str:
        pass

    @abc.abstractmethod
    def password(self) -> str:
        pass

    @abc.abstractmethod
    def internal_url(self) -> str:
        pass

    @abc.abstractmethod
    def external_url(self) -> str:
        pass

    @abc.abstractmethod
    def ui_url(self) -> str:
        pass
