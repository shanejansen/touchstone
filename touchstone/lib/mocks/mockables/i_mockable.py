import abc

from touchstone.lib.mocks.runnables.i_runnable import IRunnable


class IMockable(IRunnable):
    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_pretty_name(self):
        pass

    @abc.abstractmethod
    def get_runnable(self) -> IRunnable:
        pass
