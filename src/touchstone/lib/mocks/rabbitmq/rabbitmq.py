import http
import http.client
import urllib.error
import urllib.request
from typing import Optional

import pika

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.rabbitmq.rabbitmq_setup import RabbitmqSetup
from touchstone.lib.mocks.rabbitmq.rabbitmq_verify import RabbitmqVerify
from touchstone.lib.mocks.rabbitmq.rmq_context import RmqContext
from touchstone.lib.mocks.run_context import RunContext


class Rabbitmq(Mock):
    def __init__(self, host: str, is_dev_mode: bool, docker_manager: DockerManager):
        super().__init__(host, is_dev_mode)
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

    def is_healthy(self) -> bool:
        try:
            response = urllib.request.urlopen(f'{self.run_context.ui_url()}').read()
            return response is not None
        except (urllib.error.URLError, http.client.RemoteDisconnected):
            return False

    def run(self) -> RunContext:
        run_result = self.__docker_manager.run_image('rabbitmq:3.7.22-management-alpine', (5672, 5672),
                                                     ui_port_mapping=(15672, 15672))
        self.__container_id = run_result.container_id
        return RunContext(self._host, run_result.port, ui_port=run_result.ui_port)

    def initialize(self):
        connection_params = pika.ConnectionParameters(
            host=self._host,
            port=self.run_context.port,
            credentials=pika.PlainCredentials('guest', 'guest'),
            heartbeat=0
        )
        connection = pika.BlockingConnection(connection_params)
        rmq_context = RmqContext()
        channel = connection.channel()
        self.setup = RabbitmqSetup(channel, connection_params, rmq_context, self.config['durable'])
        self.verify = RabbitmqVerify(channel, rmq_context)

    def stop(self):
        if self.__container_id:
            self.setup.stop_listening()
            self.__docker_manager.stop_container(self.__container_id)

    def load_defaults(self, defaults: dict):
        self.setup.load_defaults(defaults)

    def reset(self):
        self.setup.reset()
