import abc


class IServiceExecutor(object):
    @abc.abstractmethod
    def execute(self, service_name: str):
        pass
