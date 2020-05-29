import abc


class IService(object):
    @abc.abstractmethod
    def get_name(self):
        pass
