from docker_manager import DockerManager
from mocks.mock import Mock


class Http(Mock):
    def __init__(self, mock_config):
        super().__init__(mock_config)
        self.container_name = None

    @staticmethod
    def name():
        return 'http'

    @staticmethod
    def pretty_name():
        return 'HTTP'

    def default_exposed_port(self):
        return 24080

    def start(self, dev_mode=False):
        self.container_name = DockerManager.instance().run_image('clue/json-server', self.exposed_port(), 80)

    def get_returns(self, url, response):
        pass
