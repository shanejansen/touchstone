from touchstone import common


class RmqContext(object):
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

    def messages_published(self, exchange: str, routing_key: str) -> int:
        return self.__exchanges[exchange][routing_key]['times']

    def payloads_published(self, exchange: str, routing_key: str) -> list:
        return self.__exchanges[exchange][routing_key]['payloads']

    def reset(self):
        for exchange in self.__exchanges:
            for routing_key in self.__exchanges[exchange]:
                self.__exchanges[exchange][routing_key]['times'] = 0
                self.__exchanges[exchange][routing_key]['payloads'] = []
