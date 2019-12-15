class RmqContext(object):
    def __init__(self):
        self.shadow_queues: dict = {}

    def add_shadow_queue(self, name: str):
        self.shadow_queues[name] = {
            'times': 0,
            'payloads': []
        }

    def increment_shadow_queue(self, name: str):
        self.shadow_queues[name]['times'] += 1

    def add_shadow_queue_payload(self, name: str, payload: str):
        self.shadow_queues[name]['payloads'].append(payload)

    def times_shadow_queue_called(self, name: str) -> int:
        return self.shadow_queues[name]['times']

    def shadow_queue_has_payload(self, name: str, payload: str) -> bool:
        return payload in self.shadow_queues[name]['payloads']
