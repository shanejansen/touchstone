import abc


class IRunnable(object):
    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def reset(self):
        pass
