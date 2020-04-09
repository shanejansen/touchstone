import urllib.error
import urllib.request
from typing import Optional

import pika

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mock_defaults import MockDefaults
from touchstone.lib.mocks.network import Network
from touchstone.lib.mocks.rabbitmq.rabbitmq_setup import RabbitmqSetup
from touchstone.lib.mocks.rabbitmq.rabbitmq_verify import RabbitmqVerify
from touchstone.lib.mocks.rabbitmq.rmq_context import RmqContext


class Rabbitmq(Mock):
    __USERNAME = 'guest'
    __PASSWORD = 'guest'

    def __init__(self, host: str, mock_defaults: MockDefaults, docker_manager: DockerManager):
        super().__init__(host, mock_defaults)
        self.setup: RabbitmqSetup = None
        self.verify: RabbitmqVerify = None
        self.__docker_manager = docker_manager
        self.__container_id: Optional[str] = None

    @staticmethod
    def name() -> str:
        return 'rabbitmq'

    @staticmethod
    def pretty_name() -> str:
        return 'Rabbit MQ'

    def default_config(self) -> dict:
        return {
            'autoCreate': True
        }

    def run(self) -> Network:
        run_result = self.__docker_manager.run_image('rabbitmq:3.7.22-management-alpine', port=5672, ui_port=15672)
        self.__container_id = run_result.container_id
        return Network(internal_host=run_result.container_id,
                       internal_port=run_result.internal_port,
                       external_port=run_result.external_port,
                       ui_port=run_result.ui_port,
                       username=self.__USERNAME,
                       password=self.__PASSWORD)

    def is_healthy(self) -> bool:
        try:
            response = urllib.request.urlopen(f'{self.network.ui_url()}').read()
            return response is not None
        except (urllib.error.URLError, ConnectionResetError):
            return False

    def initialize(self):
        connection_params = pika.ConnectionParameters(
            host=self.network.external_host,
            port=self.network.external_port,
            credentials=pika.PlainCredentials(self.__USERNAME, self.__PASSWORD),
            heartbeat=0
        )
        connection = pika.BlockingConnection(connection_params)
        rmq_context = RmqContext()
        channel = connection.channel()
        self.setup = RabbitmqSetup(channel, connection_params, rmq_context)
        self.verify = RabbitmqVerify(channel, rmq_context)
        if self.config['autoCreate']:
            self.setup.create_all(self._mock_defaults.get(self.name()))

    def services_available(self):
        if not self.config['autoCreate']:
            self.setup.create_shadow_queues(self._mock_defaults.get(self.name()))

    def reset(self):
        self.setup.purge_queues()

    def stop(self):
        if self.__container_id:
            self.setup.stop_listening()
            self.__docker_manager.stop_container(self.__container_id)
