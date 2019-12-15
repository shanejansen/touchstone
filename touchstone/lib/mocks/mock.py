import abc

from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.mocks.mock_case import Setup, Exercise, Verify


class Mock(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, mock_config: dict):
        self.mock_config: dict = mock_config

    @staticmethod
    @abc.abstractmethod
    def name() -> str:
        """The name of this mock. This is used to match the mock type in touchstone.json and defaults."""

    @staticmethod
    @abc.abstractmethod
    def pretty_name() -> str:
        """A pretty, display name for this mock."""

    def default_host(self) -> str:
        """The default host where this mock will be exposed."""
        return TouchstoneConfig.instance().config["host"]

    @abc.abstractmethod
    def default_port(self) -> int:
        """The default port where this mock will be exposed."""

    def default_endpoint(self) -> str:
        """The default endpoint where this mock will be exposed. This will simply appended to the default URL."""
        return ''

    def default_url(self) -> str:
        return f'{self.default_host()}:{self.default_port()}{self.default_endpoint()}'

    def ui_port(self) -> int:
        """Optional: The port where this mock's UI is available."""
        return self.default_port()

    def ui_endpoint(self) -> str:
        """Optional: The endpoint where this mock's UI is available."""
        return ''

    def ui_url(self):
        return f'http://{self.default_host()}:{self.ui_port()}{self.ui_endpoint()}'

    @abc.abstractmethod
    def is_healthy(self) -> bool:
        """Returns True when this mock is in a healthy state and ready to use."""

    @abc.abstractmethod
    def start(self):
        """Starts this mock."""

    def initialize(self):
        """Called when this mock becomes healthy."""
        pass

    @abc.abstractmethod
    def setup(self) -> Setup:
        """"""

    @abc.abstractmethod
    def exercise(self) -> Exercise:
        """"""

    @abc.abstractmethod
    def verify(self) -> Verify:
        """"""
