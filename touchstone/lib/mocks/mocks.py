import json
import os

import time

from touchstone.lib import exceptions
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.mocks.http.http import Http
from touchstone.lib.mocks.rabbitmq.rabbitmq import Rabbitmq


class Mocks(object):
    def __init__(self):
        self.mocks: list = []
        self.http: Http = None
        self.rabbit_mq: Rabbitmq = None

    def start(self):
        if self.mocks:
            raise exceptions.MockException('Mocks have already been started. They cannot be started again.')
        self.__parse_mocks()
        print(f'Starting mocks {[_.pretty_name() for _ in self.mocks]}...')
        for mock in self.mocks:
            mock.start()
        self.__wait_for_healthy_mocks()
        for mock in self.mocks:
            mock.initialize()
        print('Finished starting mocks.\n')

    def load_defaults(self):
        for mock in self.mocks:
            try:
                with open(os.path.join(TouchstoneConfig.instance().config['root'], f'dev-defaults/{mock.name()}.json'),
                          'r') as file:
                    defaults = json.load(file)
                    mock.setup().load_defaults(defaults)
            except FileNotFoundError:
                pass

    def cleanup(self):
        for mock in self.mocks:
            mock.setup().cleanup()

    def print_available_mocks(self):
        for mock in self.mocks:
            print(f'Mock {mock.pretty_name()} UI running at: {mock.ui_url()}')

    def __parse_mocks(self):
        for mock_config in TouchstoneConfig.instance().config['mocks']:
            mock_type = mock_config['type']
            if mock_type == Http.name():
                self.http = Http(mock_config)
                self.mocks.append(self.http)
            elif mock_type == Rabbitmq.name():
                self.rabbit_mq = Rabbitmq(mock_config)
                self.mocks.append(self.rabbit_mq)
            else:
                raise exceptions.MockNotSupportedException(
                    f'{mock_type} is not a supported mock. Please check your touchstone.json file.')

    def __wait_for_healthy_mocks(self):
        for mock in self.mocks:
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
