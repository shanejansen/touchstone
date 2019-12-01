import http
import http.client
import urllib.error
import urllib.parse
import urllib.request

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.http.http_exercise import HttpExercise
from touchstone.lib.mocks.http.http_setup import HttpSetup
from touchstone.lib.mocks.http.http_verify import HttpVerify
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mock_case import Verify, Exercise, Setup
from touchstone.lib.mocks.mock_context import MockContext


class Http(Mock):
    def __init__(self, mock_config: dict):
        super().__init__(mock_config)
        mock_context = MockContext(self.default_url())
        self.__setup = HttpSetup(mock_context)
        self.__exercise = HttpExercise(mock_context)
        self.__verify = HttpVerify(mock_context)

    @staticmethod
    def name() -> str:
        return 'http'

    @staticmethod
    def pretty_name() -> str:
        return 'HTTP'

    def default_port(self) -> int:
        return 24080

    def ui_endpoint(self) -> str:
        return '/__admin'

    def is_healthy(self) -> bool:
        try:
            response = urllib.request.urlopen(self.ui_url()).read()
            return False if response is None else True
        except (urllib.error.URLError, http.client.RemoteDisconnected):
            return False

    def start(self):
        DockerManager.instance().run_image('rodolpheche/wiremock:2.25.1-alpine', [(self.default_port(), 8080)])

    def setup(self) -> Setup:
        return self.__setup

    def exercise(self) -> Exercise:
        return self.__exercise

    def verify(self) -> Verify:
        return self.__verify
