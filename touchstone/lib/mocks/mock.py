import abc
from typing import Optional

from touchstone.lib import exceptions
from touchstone.lib.mocks.mock_defaults import MockDefaults
from touchstone.lib.mocks.network import Network
from touchstone.lib.mocks.run_context import RunContext


class Mock(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, host: str, mock_defaults: MockDefaults):
        self.config: dict = {}
        self._host = host
        self._mock_defaults = mock_defaults
        self.__network: Optional[Network] = None

    @property
    def network(self) -> Network:
        if not self.__network:
            raise exceptions.MockException('The mock must be started before its network info can be retrieved.')
        return self.__network

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

    def start(self) -> RunContext:
        """Starts this mock."""
        self.__network = self.run()
        if not self.network.external_host:
            self.__network.external_host = self._host
        return RunContext(self.name(), self.__network)

    @abc.abstractmethod
    def run(self) -> Network:
        """Runs all containers and dependencies needed to run this mock."""

    @abc.abstractmethod
    def is_healthy(self) -> bool:
        """Returns True when this mock is in a healthy state and ready to use."""

    def initialize(self):
        """Called when this mock becomes healthy."""

    def services_available(self):
        """Called when all services become available."""

    @abc.abstractmethod
    def reset(self):
        """Reset this mock to its default state."""

    @abc.abstractmethod
    def stop(self):
        """Stops this mock."""
