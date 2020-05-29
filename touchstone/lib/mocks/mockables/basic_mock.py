from touchstone.lib.mocks.mockables.i_mockable import IMockable
from touchstone.lib.mocks.runnables.i_runnable import IRunnable


class BasicMock(IMockable):
    def __init__(self, name: str, pretty_name: str, runnable: IRunnable):
        self.__name = name
        self.__pretty_name = pretty_name
        self.__runnable = runnable

    def get_name(self):
        return self.__name

    def get_pretty_name(self):
        return self.__pretty_name

    def get_runnable(self) -> IRunnable:
        return self.__runnable

    def start(self):
        self.__runnable.start()

    def stop(self):
        self.__runnable.stop()

    def reset(self):
        self.__runnable.reset()

    def services_available(self):
        self.__runnable.services_available()
