import http
import http.client
import urllib.error
import urllib.request

import pika

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mock_case import Verify, Exercise, Setup
from touchstone.lib.mocks.rabbitmq.rabbitmq_exercise import RabbitmqExercise
from touchstone.lib.mocks.rabbitmq.rabbitmq_setup import RabbitmqSetup
from touchstone.lib.mocks.rabbitmq.rabbitmq_verify import RabbitmqVerify
from touchstone.lib.mocks.rabbitmq.rmq_context import RmqContext


class Rabbitmq(Mock):
    def __init__(self, mock_config: dict):
        super().__init__(mock_config)
        self.__container_name: str = None
        self.__setup: RabbitmqSetup = None
        self.__exercise: RabbitmqExercise = None
        self.__verify: RabbitmqVerify = None

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
            return response is not None
        except (urllib.error.URLError, http.client.RemoteDisconnected):
            return False

    def start(self):
        self.__container_name = DockerManager.instance().run_image('rabbitmq:3.7.22-management-alpine',
                                                                   [(self.default_port(), 5672),
                                                                    (self.ui_port(), 15672)])

    def initialize(self):
        connection_params = pika.ConnectionParameters(
            host=self.default_host(),
            port=self.default_port(),
            credentials=pika.PlainCredentials('guest', 'guest'),
            heartbeat=0
        )
        connection = pika.BlockingConnection(connection_params)
        rmq_context = RmqContext()
        channel = connection.channel()
        self.__setup = RabbitmqSetup(channel, connection_params, rmq_context)
        self.__exercise = RabbitmqExercise(channel)
        self.__verify = RabbitmqVerify(channel)

    def stop(self):
        self.__setup.stop_listening()
        DockerManager.instance().stop_container(self.__container_name)

    def setup(self) -> Setup:
        return self.__setup

    def exercise(self) -> Exercise:
        return self.__exercise

    def verify(self) -> Verify:
        return self.__verify
