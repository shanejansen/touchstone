import exceptions
from mocks.http import Http
from mocks.rabbit_mq import RabbitMq


class Mocks(object):
    def __init__(self, touchstone_config):
        self.touchstone_config = touchstone_config
        self.mocks = []
        self.http = None
        self.rabbit_mq = None

    def start(self):
        self.__parse_mocks()
        print(f'Starting mocks {[_.pretty_name() for _ in self.mocks]}...')
        for mock in self.mocks:
            mock.start(dev_mode=self.touchstone_config['dev'])
            # TODO: wait for mocks to become healthy?
        print('Finished starting mocks.')

    def http(self):
        if self.http is None:
            raise exceptions.NotMockedException(Http.pretty_name())
        return self.http

    def rabbit_mq(self):
        if self.rabbit_mq is None:
            raise exceptions.NotMockedException(RabbitMq.pretty_name())
        return self.rabbit_mq

    def __parse_mocks(self):
        for mock in self.touchstone_config['mocks']:
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
