import pika

from touchstone.lib import exceptions
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.configurers.i_configurable import IConfigurable
from touchstone.lib.mocks.health_checks.i_url_health_checkable import IUrlHealthCheckable
from touchstone.lib.mocks.network import Network
from touchstone.lib.mocks.networked_runnables.i_networked_runnable import INetworkedRunnable
from touchstone.lib.mocks.networked_runnables.rabbitmq.docker.docker_rabbitmq_setup import DockerRabbitmqSetup
from touchstone.lib.mocks.networked_runnables.rabbitmq.docker.docker_rabbitmq_verify import DockerRabbitmqVerify
from touchstone.lib.mocks.networked_runnables.rabbitmq.i_rabbitmq_behavior import IRabbitmqBehavior, IRabbitmqVerify, \
    IRabbitmqSetup


class DockerRabbitmqRunnable(INetworkedRunnable, IRabbitmqBehavior):
    __USERNAME = 'guest'
    __PASSWORD = 'guest'

    def __init__(self, defaults_configurer: IConfigurable, configurer: IConfigurable, health_check: IUrlHealthCheckable,
                 setup: DockerRabbitmqSetup, verify: DockerRabbitmqVerify, docker_manager: DockerManager):
        self.__defaults_configurer = defaults_configurer
        self.__configurer = configurer
        self.__health_check = health_check
        self.__setup = setup
        self.__verify = verify
        self.__docker_manager = docker_manager
        self.__network = None
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
        channel = connection.channel()
        self.__setup.set_channel(channel)
        self.__setup.set_connection_params(connection_params)
        self.__verify.set_blocking_channel(channel)
        if self.__configurer.get_config()['autoCreate']:
            self.__setup.create_all(self.__defaults_configurer.get_config())

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
        if not self.__configurer.get_config()['autoCreate']:
            self.__setup.create_shadow_queues(self.__defaults_configurer.get_config())

    def is_healthy(self) -> bool:
        self.__health_check.set_url(self.get_network().ui_url())
        return self.__health_check.is_healthy()

    def setup(self) -> IRabbitmqSetup:
        if not self.__setup:
            raise exceptions.MockException('Setup unavailable. Mock is still starting.')
        return self.__setup

    def verify(self) -> IRabbitmqVerify:
        if not self.__verify:
            raise exceptions.MockException('Verify unavailable. Mock is still starting.')
        return self.__verify
