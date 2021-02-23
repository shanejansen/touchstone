import abc
from typing import Tuple, List


class IRunnable(object):
    @abc.abstractmethod
    def start(self, environment_vars: List[Tuple[str, str]] = []):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def is_running(self) -> bool:
        pass

    @abc.abstractmethod
    def wait_until_healthy(self):
        pass
