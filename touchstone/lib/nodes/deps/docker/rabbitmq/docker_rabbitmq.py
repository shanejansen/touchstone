import pika

from touchstone.lib import exceptions
from touchstone.lib.configurers.i_configurable import IConfigurable
from touchstone.lib.health_checks.http_health_check import HttpHealthCheck
from touchstone.lib.listeners.i_services_available_listener import IServicesAvailableListener
from touchstone.lib.managers.docker_manager import DockerManager
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.networking.i_network import INetwork
from touchstone.lib.nodes.deps.behaviors.i_behavior import IBehavior
from touchstone.lib.nodes.deps.behaviors.i_rabbitmq_behavior import IRabbitmqBehavior, IRabbitmqVerify, \
    IRabbitmqSetup
from touchstone.lib.nodes.deps.docker.i_runnable_docker import IRunnableDocker
from touchstone.lib.nodes.deps.docker.rabbitmq.docker_rabbitmq_setup import DockerRabbitmqSetup
from touchstone.lib.nodes.deps.docker.rabbitmq.docker_rabbitmq_verify import DockerRabbitmqVerify
from touchstone.lib.ts_context import TsContext


class DockerRabbitmq(IRunnableDocker, IRabbitmqBehavior, IServicesAvailableListener):
    __USERNAME = 'guest'
    __PASSWORD = 'guest'

    def __init__(self, ts_context: TsContext, defaults_configurer: IConfigurable, configurer: IConfigurable,
                 health_check: HttpHealthCheck, setup: DockerRabbitmqSetup, verify: DockerRabbitmqVerify,
                 docker_manager: DockerManager, docker_network: DockerNetwork):
        ts_context.register_services_available_listener(self)
        self.__defaults_configurer = defaults_configurer
        self.__configurer = configurer
        self.__health_check = health_check
        self.__setup = setup
        self.__verify = verify
        self.__docker_manager = docker_manager
        self.__docker_network = docker_network

    def get_behavior(self) -> IBehavior:
        return self

    def get_network(self) -> INetwork:
        return self.__docker_network

    def initialize(self):
        connection_params = pika.ConnectionParameters(
            host=self.__docker_network.external_host(),
            port=self.__docker_network.external_port(),
            credentials=pika.PlainCredentials(self.__USERNAME, self.__PASSWORD),
            heartbeat=0
        )
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        self.__setup.set_channel(channel)
        self.__setup.set_connection_params(connection_params)
        self.__verify.set_blocking_channel(channel)
        if self.__configurer.get_config()['auto_create']:
            self.__setup.create_all(self.__defaults_configurer.get_config())

    def start(self):
        run_result = self.__docker_manager.run_background_image('rabbitmq:3.7.22-management-alpine', port=5672,
                                                                ui_port=15672)
        self.__docker_network.set_container_id(run_result.container_id)
        self.__docker_network.set_internal_port(run_result.internal_port)
        self.__docker_network.set_external_port(run_result.external_port)
        self.__docker_network.set_ui_port(run_result.ui_port)
        self.__docker_network.set_username(self.__USERNAME)
        self.__docker_network.set_password(self.__PASSWORD)

    def stop(self):
        if self.__docker_network.container_id():
            self.__setup.stop_listening()
            self.__docker_manager.stop_container(self.__docker_network.container_id())

    def reset(self):
        self.__setup.purge_queues()

    def is_healthy(self) -> bool:
        self.__health_check.set_url(self.__docker_network.ui_url())
        return self.__health_check.is_healthy()

    def setup(self) -> IRabbitmqSetup:
        if not self.__setup:
            raise exceptions.DepException('Setup unavailable. Dependency is still starting.')
        return self.__setup

    def verify(self) -> IRabbitmqVerify:
        if not self.__verify:
            raise exceptions.DepException('Verify unavailable. Dependency is still starting.')
        return self.__verify

    def services_available(self):
        if not self.__configurer.get_config()['auto_create']:
            self.__setup.create_shadow_queues(self.__defaults_configurer.get_config())
