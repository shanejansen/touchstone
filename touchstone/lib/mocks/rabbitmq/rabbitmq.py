import http
import http.client
import urllib.error
import urllib.request

from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mock_case import Verify, Exercise, Setup


class Rabbitmq(Mock):

    @staticmethod
    def name() -> str:
        return 'rabbitmq'

    @staticmethod
    def pretty_name() -> str:
        return 'Rabbit MQ'

    def default_port(self) -> int:
        return 24672

    def ui_port(self) -> int:
        return 24172

    def is_healthy(self) -> bool:
        try:
            response = urllib.request.urlopen(f'{self.ui_url()}').read()
            return False if response is None else True
        except (urllib.error.URLError, http.client.RemoteDisconnected):
            return False

    def start(self):
        dev_ports = None
        if TouchstoneConfig.instance().config['dev']:
            dev_ports = [15672]
        DockerManager.instance().run_image('rabbitmq:3.7.22-management-alpine', self.exposed_port(), 5672,
                                           dev_ports=dev_ports)

    def setup(self) -> Setup:
        pass

    def exercise(self) -> Exercise:
        pass

    def verify(self) -> Verify:
        pass
