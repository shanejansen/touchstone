class RmqContext(object):
    def __init__(self):
        self.__shadow_queues: dict = {}

    def add_shadow_queue(self, name: str):
        self.__shadow_queues[name] = {
            'times': 0,
            'payloads': []
        }

    def shadow_queue_payload_received(self, name: str, payload: str):
        self.__shadow_queues[name]['payloads'].append(payload)
        self.__shadow_queues[name]['times'] += 1

    def times_shadow_queue_called(self, name: str) -> int:
        return self.__shadow_queues[name]['times']

    def shadow_queue_has_payload(self, name: str, payload: str) -> bool:
        return payload in self.__shadow_queues[name]['payloads']

    def reset(self):
        for shadow_queue in self.__shadow_queues:
            self.__shadow_queues[shadow_queue]['times'] = 0
            self.__shadow_queues[shadow_queue]['payloads'] = []
