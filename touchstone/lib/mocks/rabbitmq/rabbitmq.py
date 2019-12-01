import http
import http.client
import urllib.error
import urllib.request

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mock_case import Verify, Exercise, Setup
from touchstone.lib.mocks.mock_context import MockContext
from touchstone.lib.mocks.rabbitmq.rabbitmq_exercise import RabbitmqExercise
from touchstone.lib.mocks.rabbitmq.rabbitmq_setup import RabbitmqSetup
from touchstone.lib.mocks.rabbitmq.rabbitmq_verify import RabbitmqVerify


class Rabbitmq(Mock):
    def __init__(self, mock_config: dict):
        super().__init__(mock_config)
        mock_context = MockContext(self.default_url())
        self.__setup = RabbitmqSetup(mock_context)
        self.__exercise = RabbitmqExercise(mock_context)
        self.__verify = RabbitmqVerify(mock_context)

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
            return False if response is None else True
        except (urllib.error.URLError, http.client.RemoteDisconnected):
            return False

    def start(self):
        DockerManager.instance().run_image('rabbitmq:3.7.22-management-alpine',
                                           [(self.default_port(), 5672),
                                            (self.ui_port(), 15672)])

    def setup(self) -> Setup:
        return self.__setup

    def exercise(self) -> Exercise:
        return self.__exercise

    def verify(self) -> Verify:
        return self.__verify
