from touchstone import common


class DockerRabbitmqContext(object):
    def __init__(self):
        self.__exchanges: dict = {}

    def track(self, exchange: str, routing_key: str):
        if exchange not in self.__exchanges:
            self.__exchanges[exchange] = {}
        self.__exchanges[exchange][routing_key] = {
            'times': 0,
            'payloads': []
        }
        common.logger.debug(f'Now tracking: {self.__exchanges}')

    def track_payload(self, exchange: str, routing_key: str, payload: str):
        self.__exchanges[exchange][routing_key]['times'] += 1
        self.__exchanges[exchange][routing_key]['payloads'].append(payload)

    def exchange_is_tracked(self, exchange: str, routing_key: str, print_warning=True) -> bool:
        if exchange in self.__exchanges and routing_key in self.__exchanges[exchange]:
            return True
        if print_warning:
            print(f'This exchange: "{exchange}", routing-key: "{routing_key}" combination is not defined. Check your '
                  f'"rabbitmq.yml" defaults.')
        return False

    def messages_published(self, exchange: str, routing_key: str) -> int:
        return self.__exchanges[exchange][routing_key]['times']

    def payloads_published(self, exchange: str, routing_key: str) -> list:
        return self.__exchanges[exchange][routing_key]['payloads']

    def clear(self):
        for exchange in self.__exchanges:
            for routing_key in self.__exchanges[exchange]:
                self.__exchanges[exchange][routing_key]['times'] = 0
                self.__exchanges[exchange][routing_key]['payloads'] = []
