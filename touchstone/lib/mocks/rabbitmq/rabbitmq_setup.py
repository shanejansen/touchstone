from threading import Thread

from pika import spec
from pika.adapters.blocking_connection import BlockingChannel

from touchstone.lib.mocks.mock_case import Setup
from touchstone.lib.mocks.rabbitmq.rmq_context import RmqContext


class RabbitmqSetup(Setup):
    def __init__(self, channel: BlockingChannel, rmq_context: RmqContext):
        super().__init__()
        self.channel: BlockingChannel = channel
        self.rmq_context: RmqContext = rmq_context

        self.exchanges: list = []
        self.queues: list = []
        self.default_exchanges: list = []
        self.default_queues = []

    def load_defaults(self, defaults: dict):
        for exchange in defaults['exchanges']:
            self.__create_default_exchange(exchange['name'], exchange['type'])
            for queue in exchange['queues']:
                routing_key = queue.get('routingKey', None)
                self.__create_default_queue(queue['name'], exchange['name'], routing_key)
        consuming_thread = Thread(target=self.channel.start_consuming)
        consuming_thread.start()

    def reset(self):
        for queue in self.queues:
            self.channel.queue_delete(queue)
        self.queues = []
        for exchange in self.exchanges:
            self.channel.exchange_delete(exchange=exchange)
        self.exchanges = []

        for default_queue in self.default_queues:
            self.channel.queue_purge(default_queue)

    def create_exchange(self, name: str, exchange_type: str = 'direct'):
        if name not in self.exchanges:
            self.channel.exchange_declare(name, exchange_type=exchange_type)
            self.exchanges.append(name)

    def __create_default_exchange(self, name: str, exchange_type: str = 'direct'):
        if name not in self.default_exchanges:
            self.channel.exchange_declare(name, exchange_type=exchange_type)
            self.default_exchanges.append(name)

            shadow_queue = name + '.touchstone-shadow'
            self.__create_default_queue(shadow_queue, name)
            self.rmq_context.add_shadow_queue(shadow_queue)
            self.__consume(shadow_queue)

    def create_queue(self, name: str, exchange: str, routing_key: str = None):
        if name not in self.queues:
            self.channel.queue_declare(name)
            self.channel.queue_bind(name, exchange, routing_key=routing_key)
            self.queues.append(name)

    def __create_default_queue(self, name: str, exchange: str, routing_key: str = None):
        if name not in self.default_queues:
            self.channel.queue_declare(name)
            self.channel.queue_bind(name, exchange, routing_key=routing_key)
            self.default_queues.append(name)

    def __consume(self, queue_name: str):
        def message_received(channel: BlockingChannel, method: spec.Basic.Deliver, properties: spec.BasicProperties,
                             body: bytes):
            print(method)
            print(properties)
            print(body)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue_name, message_received)
