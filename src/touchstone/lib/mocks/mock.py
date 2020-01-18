import abc
from typing import Optional

from touchstone.lib import exceptions
from touchstone.lib.mocks.run_context import RunContext


class Mock(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, host: str, is_dev_mode: bool):
        self.config: dict = {}
        self._host = host
        self._is_dev_mode = is_dev_mode
        self.__run_context: Optional[RunContext] = None

    @property
    def run_context(self) -> RunContext:
        if not self.__run_context:
            raise exceptions.MockException('The mock must be started before its run context can be retrieved.')
        return self.__run_context

    @staticmethod
    @abc.abstractmethod
    def name() -> str:
        """The name of this mock. This is used to match the mock type in touchstone.yml and defaults."""

    @staticmethod
    @abc.abstractmethod
    def pretty_name() -> str:
        """A pretty, display name for this mock."""

    def default_config(self) -> dict:
        """Optional: A dictionary of configuration values with defaults for this mock. This will be available via
        'self.config'."""
        return {}

    def start(self):
        """Starts this mock."""
        self.__run_context = self.run()

    @abc.abstractmethod
    def run(self) -> RunContext:
        """Runs all containers and dependencies needed to run this mock."""

    def initialize(self):
        """Called when this mock becomes healthy."""

    @abc.abstractmethod
    def is_healthy(self) -> bool:
        """Returns True when this mock is in a healthy state and ready to use."""

    @abc.abstractmethod
    def stop(self):
        """Stops this mock."""

    @abc.abstractmethod
    def load_defaults(self, defaults: dict):
        """Loads defaults for this mock provided by the user."""

    @abc.abstractmethod
    def reset(self):
        """Returns this mock to its original state."""
