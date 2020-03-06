import time
from typing import List

from touchstone import common
from touchstone.lib import exceptions
from touchstone.lib.mocks.http.http import Http
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mongodb.mongodb import Mongodb
from touchstone.lib.mocks.mysql.mysql import Mysql
from touchstone.lib.mocks.rabbitmq.rabbitmq import Rabbitmq
from touchstone.lib.mocks.run_context import RunContext
from touchstone.lib.mocks.s3.s3 import S3


class Mocks(object):
    def __init__(self):
        self.http: Http = None
        self.rabbitmq: Rabbitmq = None
        self.mongodb: Mongodb = None
        self.mysql: Mysql = None
        self.s3: S3 = None
        self.__registered_mocks: List[Mock] = []
        self.__mocks_running = False

    def register_mock(self, mock: Mock):
        self.__registered_mocks.append(mock)

    def start(self) -> List[RunContext]:
        if self.__mocks_running:
            print('Mocks have already been started. They cannot be started again.')
        else:
            print(f'Starting mocks {[_.pretty_name() for _ in self.__registered_mocks]}...')
            run_contexts = []
            for mock in self.__registered_mocks:
                run_contexts.append(mock.start())
            self.__wait_for_healthy_mocks()
            for mock in self.__registered_mocks:
                mock.initialize()
            self.__mocks_running = True
            print('Finished starting mocks.\n')
            return run_contexts

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
            message = f'Mock {mock.pretty_name()} UI running at: {mock.network.ui_url()}'
            if mock.network.username:
                message += f' Username: "{mock.network.username}", Password: "{mock.network.password}"'
            print(message)

    def __wait_for_healthy_mocks(self):
        for mock in self.__registered_mocks:
            attempt = 0
            healthy = False
            while not healthy and attempt is not 10:
                attempt += 1
                common.logger.debug(f'Waiting for mock: {mock.name()} to become healthy. Attempt {attempt} of 10.')
                if mock.is_healthy():
                    healthy = True
                    attempt = 0
                else:
                    time.sleep(5)
            if attempt is 10:
                raise exceptions.MockException(
                    f'Mock {mock.pretty_name()} never became healthy and timed out on initialization.')
