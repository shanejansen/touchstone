import exceptions
from mocks.http import Http
from mocks.rabbit_mq import RabbitMq
from touchstone_config import TouchstoneConfig


class Mocks(object):
    def __init__(self):
        self.mocks = []
        self.http = None
        self.rabbit_mq = None

    def start(self):
        self.__parse_mocks()
        print(f'Starting mocks {[_.pretty_name() for _ in self.mocks]}...')
        for mock in self.mocks:
            mock.start()
            # TODO: wait for mocks to become healthy?
        print('Finished starting mocks.')

    def cleanup(self):
        for mock in self.mocks:
            mock.cleanup()

    def print_available_mocks(self):
        for mock in self.mocks:
            print(
                f'Mock {mock.pretty_name()} running on: '
                f'http://{TouchstoneConfig.instance().config["host"]}/{mock.exposed_port()}')

    def __parse_mocks(self):
        for mock in TouchstoneConfig.instance().config['mocks']:
            mock_type = mock['type']
            if mock_type == Http.name():
                self.http = Http(mock)
                self.mocks.append(self.http)
            elif mock_type == RabbitMq.name():
                self.rabbit_mq = RabbitMq(mock)
                self.mocks.append(self.rabbit_mq)
            else:
                raise exceptions.MockNotSupportedException(
                    f'{mock_type} is not a supported mock. Please check your touchstone.json file.')
