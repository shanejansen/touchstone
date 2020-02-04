import urllib.error
import urllib.request
from typing import Optional

import pika

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.network import Network
from touchstone.lib.mocks.rabbitmq.rabbitmq_setup import RabbitmqSetup
from touchstone.lib.mocks.rabbitmq.rabbitmq_verify import RabbitmqVerify
from touchstone.lib.mocks.rabbitmq.rmq_context import RmqContext


class Rabbitmq(Mock):
    def __init__(self, host: str, docker_manager: DockerManager):
        super().__init__(host)
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
            'durable': False
        }

    def run(self) -> Network:
        run_result = self.__docker_manager.run_image('rabbitmq:3.7.22-management-alpine', port=5672, ui_port=15672)
        self.__container_id = run_result.container_id
        return Network(internal_host=run_result.container_id,
                       internal_port=run_result.internal_port,
                       external_port=run_result.external_port,
                       ui_port=run_result.ui_port)

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
            credentials=pika.PlainCredentials('guest', 'guest'),
            heartbeat=0
        )
        connection = pika.BlockingConnection(connection_params)
        rmq_context = RmqContext()
        channel = connection.channel()
        self.setup = RabbitmqSetup(channel, connection_params, rmq_context, self.config['durable'])
        self.verify = RabbitmqVerify(channel, rmq_context)

    def load_defaults(self, defaults: dict):
        self.setup.load_defaults(defaults)

    def stop(self):
        if self.__container_id:
            self.setup.stop_listening()
            self.__docker_manager.stop_container(self.__container_id)
