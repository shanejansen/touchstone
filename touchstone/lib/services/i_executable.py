import abc


class IExecutable(object):
    @abc.abstractmethod
    def execute(self):
        pass
