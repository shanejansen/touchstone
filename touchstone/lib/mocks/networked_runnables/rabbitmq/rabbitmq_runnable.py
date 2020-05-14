import pika

from touchstone.lib import exceptions
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.configurers.BasicConfigurer import BasicConfigurer
from touchstone.lib.mocks.health_checks.http_health_check import HttpHealthCheck
from touchstone.lib.mocks.network import Network
from touchstone.lib.mocks.networked_runnables.i_networked_runnable import INetworkedRunnable
from touchstone.lib.mocks.networked_runnables.rabbitmq.i_rabbitmq_behavior import IRabbitmqBehavior
from touchstone.lib.mocks.networked_runnables.rabbitmq.rabbitmq_context import RmqContext
from touchstone.lib.mocks.networked_runnables.rabbitmq.rabbitmq_setup import RabbitmqSetup
from touchstone.lib.mocks.networked_runnables.rabbitmq.rabbitmq_verify import RabbitmqVerify


class RabbitmqRunnable(INetworkedRunnable, IRabbitmqBehavior):
    __USERNAME = 'guest'
    __PASSWORD = 'guest'
    __DEFAULT_CONFIG = {
        'autoCreate': True
    }

    def __init__(self, defaults: dict, config: dict, docker_manager: DockerManager):
        self.__defaults = defaults
        self.__config = BasicConfigurer(self.__DEFAULT_CONFIG)
        self.__config.merge_config(config)
        self.__docker_manager = docker_manager
        self.__health_check = HttpHealthCheck()
        self.__network = None
        self.__setup = None
        self.__verify = None
        self.__container_id = None

    def get_network(self) -> Network:
        if not self.__network:
            raise exceptions.MockException('Network unavailable. Mock is still starting.')
        return self.__network

    def initialize(self):
        connection_params = pika.ConnectionParameters(
            host=self.get_network().external_host,
            port=self.get_network().external_port,
            credentials=pika.PlainCredentials(self.__USERNAME, self.__PASSWORD),
            heartbeat=0
        )
        connection = pika.BlockingConnection(connection_params)
        rmq_context = RmqContext()
        channel = connection.channel()
        self.__setup = RabbitmqSetup(channel, connection_params, rmq_context)
        self.__verify = RabbitmqVerify(channel, rmq_context)
        if self.__config.get_config()['autoCreate']:
            self.__setup.create_all(self.__defaults)

    def start(self):
        run_result = self.__docker_manager.run_image('rabbitmq:3.7.22-management-alpine', port=5672, ui_port=15672)
        self.__container_id = run_result.container_id
        self.__network = Network(internal_host=run_result.container_id,
                                 internal_port=run_result.internal_port,
                                 external_port=run_result.external_port,
                                 ui_port=run_result.ui_port,
                                 username=self.__USERNAME,
                                 password=self.__PASSWORD)

    def stop(self):
        if self.__container_id:
            self.__setup.stop_listening()
            self.__docker_manager.stop_container(self.__container_id)

    def reset(self):
        self.__setup.purge_queues()

    def services_available(self):
        if not self.__config.get_config()['autoCreate']:
            self.__setup.create_shadow_queues(self.__defaults)

    def is_healthy(self) -> bool:
        self.__health_check.set_url(self.get_network().ui_url())
        return self.__health_check.is_healthy()

    def setup(self) -> RabbitmqSetup:
        if not self.__setup:
            raise exceptions.MockException('Setup unavailable. Mock is still starting.')
        return self.__setup

    def verify(self) -> RabbitmqVerify:
        if not self.__verify:
            raise exceptions.MockException('Verify unavailable. Mock is still starting.')
        return self.__verify
