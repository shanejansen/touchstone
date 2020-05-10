import time
from typing import List

from touchstone import common
from touchstone.lib import exceptions
from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.health_checks.i_health_checkable import IHealthCheckable
from touchstone.lib.mocks.mockables.i_mockable import IMockable
from touchstone.lib.mocks.mockables.networked_mock import NetworkedMock
from touchstone.lib.mocks.networked_runnables.http.http_runnable import HttpRunnable
from touchstone.lib.mocks.networked_runnables.http.i_http_behavior import IHttpBehavior
from touchstone.lib.mocks.networked_runnables.i_networked_runnable import INetworkedRunnable
from touchstone.lib.mocks.networked_runnables.rabbitmq.i_rabbitmq_behavior import IRabbitmqBehavior
from touchstone.lib.mocks.networked_runnables.rabbitmq.rabbitmq_runnable import RabbitmqRunnable


class Mocks(object):
    __HTTP = 'http'
    __RABBITMQ = 'rabbitmq'

    def __init__(self):
        self.http: IHttpBehavior = None
        self.rabbitmq: IRabbitmqBehavior = None
        # self.mongodb: Mongodb = None
        # self.mysql: Mysql = None
        # self.s3: S3 = None
        self.__registered_mocks: List[IMockable] = []
        self.__mocks_running = False

    def register_mocks(self, mocks_config: dict, mocks_defaults: dict, docker_manager: DockerManager, host: str):
        for mock_name in mocks_config:
            mock = None
            mock_config = mocks_config.get(mock_name, {})
            mock_defaults = mocks_defaults.get(mock_name, {})
            if mock_name == self.__HTTP:
                runnable = HttpRunnable(mock_defaults, docker_manager)
                mock = NetworkedMock(self.__HTTP, 'HTTP', host, runnable)
                self.http = runnable
            elif mock_name == self.__RABBITMQ:
                runnable = RabbitmqRunnable(mock_defaults, mock_config, docker_manager)
                mock = NetworkedMock(self.__RABBITMQ, 'Rabbit MQ', host, runnable)
                self.rabbitmq = runnable
            if mock:
                self.__registered_mocks.append(mock)

    def start(self):
        if self.__mocks_running:
            print('Mocks have already been started. They cannot be started again.')
        else:
            print(f'Starting mocks {[_.get_pretty_name() for _ in self.__registered_mocks]}...')
            for mock in self.__registered_mocks:
                mock.start()
            self.__wait_for_healthy_mocks()
            self.__mocks_running = True
            print('Finished starting mocks.\n')

    def stop(self):
        print('Stopping mocks...')
        for mock in self.__registered_mocks:
            mock.stop()
        self.__mocks_running = False

    def are_running(self):
        return self.__mocks_running

    def services_became_available(self):
        for mock in self.__registered_mocks:
            mock.services_available()

    def reset(self):
        for mock in self.__registered_mocks:
            mock.reset()

    def print_available_mocks(self):
        for mock in self.__registered_mocks:
            message = f'Mock {mock.get_pretty_name()} running'
            if isinstance(mock, INetworkedRunnable):
                message += f' with UI: {mock.get_network().ui_url()}'
                if mock.get_network().username:
                    message += f' and Username: "{mock.get_network().username}", ' \
                               f'Password: "{mock.get_network().password}"'
            print(message)

    def __wait_for_healthy_mocks(self):
        for mock in self.__registered_mocks:
            health_checkable = mock
            if isinstance(health_checkable, IHealthCheckable):
                attempt = 0
                healthy = False
                while not healthy and attempt is not 10:
                    attempt += 1
                    common.logger.debug(
                        f'Waiting for mock: {mock.get_name()} to become healthy. Attempt {attempt} of 10.')
                    if health_checkable.is_healthy():
                        healthy = True
                        attempt = 0
                    else:
                        time.sleep(5)
                if attempt is 10:
                    raise exceptions.MockException(
                        f'Mock {mock.get_pretty_name()} never became healthy and timed out on initialization.')
