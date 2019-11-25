import abc

from touchstone.lib.mocks.mock_case import Setup, Exercise, Verify


class Mock(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, mock_config: dict):
        self.mock_config: dict = mock_config

    @staticmethod
    @abc.abstractmethod
    def name() -> str:
        """The name of this mock. This is used to match the mock type in touchstone.json and dev-defaults"""

    @staticmethod
    @abc.abstractmethod
    def pretty_name() -> str:
        """A pretty, display name for this mock"""

    @abc.abstractmethod
    def default_exposed_port(self) -> int:
        """The default port where this mock will be exposed. Be sure to call the method self.exposed_port() in case it
        has been overridden"""

    @abc.abstractmethod
    def is_healthy(self) -> bool:
        """Returns True when this mock is in a healthy state and ready to use."""

    @abc.abstractmethod
    def start(self):
        """Starts this mock"""

    @abc.abstractmethod
    def setup(self) -> Setup:
        """"""

    @abc.abstractmethod
    def exercise(self) -> Exercise:
        """"""

    @abc.abstractmethod
    def verify(self) -> Verify:
        """"""

    def exposed_port(self) -> int:
        if 'port' in self.mock_config:
            return self.mock_config['port']
        return self.default_exposed_port()
