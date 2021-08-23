import abc


class IServicesAvailableListener(object):
    @abc.abstractmethod
    def services_available(self):
        pass
