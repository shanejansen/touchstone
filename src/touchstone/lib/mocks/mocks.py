import os
import time
from typing import List

import yaml

from touchstone import common
from touchstone.lib import exceptions
from touchstone.lib.mocks.http.http import Http
from touchstone.lib.mocks.mongodb.mongodb import Mongodb
from touchstone.lib.mocks.mysql.mysql import Mysql
from touchstone.lib.mocks.rabbitmq.rabbitmq import Rabbitmq
from touchstone.lib.mocks.run_context import RunContext


class Mocks(object):
    def __init__(self, root: str, http: Http, rabbitmq: Rabbitmq, mongodb: Mongodb, mysql: Mysql):
        self.http: Http = http
        self.rabbitmq: Rabbitmq = rabbitmq
        self.mongodb: Mongodb = mongodb
        self.mysql: Mysql = mysql
        self.__root = root
        self.__mocks = [http, rabbitmq, mongodb, mysql]
        self.__mocks_running = False

    def start(self) -> List[RunContext]:
        if self.__mocks_running:
            print('Mocks have already been started. They cannot be started again.')
        else:
            print(f'Starting mocks {[_.pretty_name() for _ in self.__mocks]}...')
            run_contexts = []
            for mock in self.__mocks:
                run_contexts.append(mock.start())
            self.__wait_for_healthy_mocks()
            for mock in self.__mocks:
                mock.initialize()
            self.__mocks_running = True
            print('Finished starting mocks.\n')
            return run_contexts

    def stop(self):
        print('Stopping mocks...')
        for mock in self.__mocks:
            mock.stop()
        self.__mocks_running = False

    def are_running(self):
        return self.__mocks_running

    def load_defaults(self):
        for mock in self.__mocks:
            try:
                with open(os.path.join(self.__root, f'defaults/{mock.name()}.yml'), 'r') as file:
                    defaults = yaml.safe_load(file)
                    mock.load_defaults(defaults)
            except FileNotFoundError:
                pass

    def print_available_mocks(self):
        for mock in self.__mocks:
            print(f'Mock {mock.pretty_name()} UI running at: {mock.network.ui_url()}')

    def __wait_for_healthy_mocks(self):
        for mock in self.__mocks:
            retries = 0
            healthy = False
            while not healthy and retries is not 10:
                retries += 1
                common.logger.debug(f'Waiting for mock: {mock.name()} to become healthy. Retry {retries} of 10.')
                if mock.is_healthy():
                    healthy = True
                    retries = 0
                else:
                    time.sleep(5)
            if retries is 10:
                raise exceptions.MockException(
                    f'Mock {mock.pretty_name()} never became healthy and timed out on initialization.')
