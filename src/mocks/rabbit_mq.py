from docker_manager import DockerManager
from mocks.mock import Mock


class RabbitMq(Mock):
    @staticmethod
    def name():
        return 'rabbitmq'

    @staticmethod
    def pretty_name():
        return 'Rabbit MQ'

    def default_exposed_port(self):
        return 24672

    def start(self, dev_mode=False):
        DockerManager.instance().run_image('rabbitmq:management-alpine', self.exposed_port(), 5672, dev_ports=[15672])
