import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.http.http_setup import HttpSetup
from touchstone.lib.mocks.http.http_verify import HttpVerify
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.network import Network


class Http(Mock):
    def __init__(self, host: str, docker_manager: DockerManager):
        super().__init__(host)
        self.setup: HttpSetup = None
        self.verify: HttpVerify = None
        self.__docker_manager = docker_manager
        self.__container_id: Optional[str] = None

    @staticmethod
    def name() -> str:
        return 'http'

    @staticmethod
    def pretty_name() -> str:
        return 'HTTP'

    def run(self) -> Network:
        run_result = self.__docker_manager.run_image('rodolpheche/wiremock:2.25.1-alpine', port=8080, exposed_port=8081)
        self.__container_id = run_result.container_id
        return Network(network_host=run_result.container_id,
                       port=run_result.port,
                       network_port=run_result.network_port,
                       prefix='http://',
                       ui_endpoint='/__admin')

    def is_healthy(self) -> bool:
        try:
            response = urllib.request.urlopen(self.network.ui_url()).read()
            return False if response is None else True
        except (urllib.error.URLError, ConnectionResetError):
            return False

    def initialize(self):
        self.setup: HttpSetup = HttpSetup(self.network.url())
        self.verify: HttpVerify = HttpVerify(self.network.url())

    def load_defaults(self, defaults: dict):
        self.setup.load_defaults(defaults)

    def stop(self):
        if self.__container_id:
            self.__docker_manager.stop_container(self.__container_id)
