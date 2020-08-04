import abc
from typing import Tuple, List


class IExecutable(object):
    @abc.abstractmethod
    def execute(self, environment_vars: List[Tuple[str, str]] = []):
        pass
