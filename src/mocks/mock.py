import abc
from typing import Dict


class Mock(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, mock_config):
        self.mock_config = mock_config

    @staticmethod
    def name() -> str:
        """The name of this mock. This is used to match the mock type in touchstone.json and mock-defaults"""

    @staticmethod
    def pretty_name() -> str:
        """A pretty, display name for this mock"""

    @abc.abstractmethod
    def default_exposed_port(self) -> str:
        """The default port where this mock will be exposed. Be sure to call the method self.exposed_port() in case it
        has been overridden"""

    @abc.abstractmethod
    def is_healthy(self) -> bool:
        """Returns True when this mock is in a healthy state and ready to use."""

    @abc.abstractmethod
    def start(self):
        """Starts this mock"""

    @abc.abstractmethod
    def load_defaults(self, defaults: Dict):
        """Load defaults for this mock provided by the user for dev purposes"""

    @abc.abstractmethod
    def cleanup(self):
        """Cleanup this mock to prepare for the next test"""

    def exposed_port(self) -> str:
        if 'port' in self.mock_config:
            return self.mock_config['port']
        return self.default_exposed_port()
