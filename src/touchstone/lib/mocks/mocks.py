import os
import time

import yaml

from touchstone.lib import exceptions
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.mocks.http.http import Http
from touchstone.lib.mocks.rabbitmq.rabbitmq import Rabbitmq


class Mocks(object):
    def __init__(self):
        self.http: Http = None
        self.rabbit_mq: Rabbitmq = None
        self.__mocks: list = self.__parse_mocks()
        self.__mocks_running = False

    def start(self):
        if self.__mocks_running:
            print('Mocks have already been started. They cannot be started again.')
        else:
            print(f'Starting mocks {[_.pretty_name() for _ in self.__mocks]}...')
            for mock in self.__mocks:
                mock.start()
            self.__wait_for_healthy_mocks()
            for mock in self.__mocks:
                mock.initialize()
            self.__mocks_running = True
            print('Finished starting mocks.\n')

    def stop(self):
        print('Stopping mocks...')
        for mock in self.__mocks:
            mock.stop()
        self.__mocks_running = False

    def load_defaults(self):
        for mock in self.__mocks:
            try:
                with open(os.path.join(TouchstoneConfig.instance().config['root'], f'defaults/{mock.name()}.yml'),
                          'r') as file:
                    defaults = yaml.safe_load(file)
                    mock.load_defaults(defaults)
            except FileNotFoundError:
                pass

    def reset(self):
        for mock in self.__mocks:
            mock.reset()

    def print_available_mocks(self):
        for mock in self.__mocks:
            print(f'Mock {mock.pretty_name()} UI running at: {mock.ui_url()}')

    def __parse_mocks(self) -> list:
        mocks = []
        for mock_config in TouchstoneConfig.instance().config['mocks']:
            if Http.name() == mock_config:
                self.http = Http(mock_config)
                mocks.append(self.http)
            elif Rabbitmq.name() == mock_config:
                self.rabbit_mq = Rabbitmq(mock_config)
                mocks.append(self.rabbit_mq)
            else:
                raise exceptions.MockNotSupportedException(
                    f'{mock_config} is not a supported mock. Please check your touchstone.yml file.')
        return mocks

    def __wait_for_healthy_mocks(self):
        for mock in self.__mocks:
            retries = 0
            healthy = False
            while not healthy and retries is not 10:
                retries += 1
                if mock.is_healthy():
                    healthy = True
                    retries = 0
                else:
                    time.sleep(5)
            if retries is 10:
                raise exceptions.MockException(
                    f'Mock {mock.pretty_name()} never became healthy and timed out on initialization.')
