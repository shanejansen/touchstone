from pika.adapters.blocking_connection import BlockingChannel

from touchstone.lib.mocks.mock_case import Setup


class RabbitmqSetup(Setup):
    def __init__(self, channel: BlockingChannel):
        super().__init__()
        self.channel: BlockingChannel = channel

        # Create original queue
        # Create shadow queue
        # Add to shadow queue dictionary
        # Listed to shadow queue
        # Update dictionary as messages are received
        test = {
            'queue.name': {
                'times': 0,
                'payloads': {
                    "",
                    ""
                }
            }
        }

        self.exchanges: list = []
        self.queues: list = []

    def load_defaults(self, defaults: dict):
        for exchange in defaults['exchanges']:
            self.create_exchange(exchange['name'], exchange['type'])
            for queue in exchange['queues']:
                routing_key = queue.get('routingKey', None)
                self.create_queue(queue['name'], exchange['name'], routing_key)

    def cleanup(self):
        for queue in self.queues:
            self.channel.queue_delete(queue)
        self.queues = []
        for exchange in self.exchanges:
            self.channel.exchange_delete(exchange=exchange)
        self.exchanges = []

    def create_exchange(self, name: str, exchange_type: str = 'direct'):
        if name not in self.exchanges:
            self.channel.exchange_declare(name, exchange_type=exchange_type)
            self.exchanges.append(name)

    def create_queue(self, name: str, exchange: str, routing_key: str = None):
        if name not in self.queues:
            self.channel.queue_declare(name)
            self.channel.queue_bind(name, exchange, routing_key=routing_key)
            self.queues.append(name)
