from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock


class RabbitMq(Mock):
    @staticmethod
    def name():
        return 'rabbitmq'

    def default_exposed_port(self):
        return 24672

    @staticmethod
    def pretty_name():
        return 'Rabbit MQ'

    def is_healthy(self) -> bool:
        pass

    def start(self, dev_mode=False):
        DockerManager.instance().run_image('rabbitmq:management-alpine', self.exposed_port(), 5672, dev_ports=[15672])

    def cleanup(self):
        pass
