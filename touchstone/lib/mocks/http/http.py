import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.http.http_setup import HttpSetup
from touchstone.lib.mocks.http.http_verify import HttpVerify
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mock_defaults import MockDefaults
from touchstone.lib.mocks.network import Network


class Http(Mock):
    def __init__(self, host: str, mock_defaults: MockDefaults, docker_manager: DockerManager):
        super().__init__(host, mock_defaults)
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
        run_result = self.__docker_manager.run_image('holomekc/wiremock-gui:2.25.1', port=8080, exposed_port=9090)
        self.__container_id = run_result.container_id
        return Network(internal_host=run_result.container_id,
                       internal_port=run_result.internal_port,
                       external_port=run_result.external_port,
                       ui_port=run_result.ui_port,
                       ui_endpoint='/__admin/webapp',
                       prefix='http://')

    def is_healthy(self) -> bool:
        try:
            response = urllib.request.urlopen(self.network.ui_url()).read()
            return False if response is None else True
        except (urllib.error.URLError, ConnectionResetError):
            return False

    def initialize(self):
        self.setup: HttpSetup = HttpSetup(self.network.external_url())
        self.verify: HttpVerify = HttpVerify(self.network.external_url())
        self.setup.init(self._mock_defaults.get(self.name()))

    def reset(self):
        self.setup.init(self._mock_defaults.get(self.name()))

    def stop(self):
        if self.__container_id:
            self.__docker_manager.stop_container(self.__container_id)
