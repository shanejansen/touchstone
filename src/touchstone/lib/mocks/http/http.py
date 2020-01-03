import http
import http.client
import urllib.error
import urllib.parse
import urllib.request

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.http.http_setup import HttpSetup
from touchstone.lib.mocks.http.http_verify import HttpVerify
from touchstone.lib.mocks.mock import Mock


class Http(Mock):
    def __init__(self):
        super().__init__()
        self.setup: HttpSetup = HttpSetup(self.default_url())
        self.verify: HttpVerify = HttpVerify(self.default_url())
        self.__container_name: str = None

    @staticmethod
    def name() -> str:
        return 'http'

    @staticmethod
    def pretty_name() -> str:
        return 'HTTP'

    def default_port(self) -> int:
        return 8081

    def default_url(self) -> str:
        return 'http://' + super().default_url()

    def ui_endpoint(self) -> str:
        return '/__admin'

    def is_healthy(self) -> bool:
        try:
            response = urllib.request.urlopen(self.ui_url()).read()
            return False if response is None else True
        except (urllib.error.URLError, http.client.RemoteDisconnected):
            return False

    def start(self):
        self.__container_name = DockerManager.instance().run_image('rodolpheche/wiremock:2.25.1-alpine',
                                                                   [(self.default_port(), 8080)])

    def stop(self):
        DockerManager.instance().stop_container(self.__container_name)

    def load_defaults(self, defaults: dict):
        self.setup.load_defaults(defaults)

    def reset(self):
        self.setup.reset()
