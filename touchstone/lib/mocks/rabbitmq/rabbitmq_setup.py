from threading import Thread

import pika
from pika import spec
from pika.adapters.blocking_connection import BlockingChannel

from touchstone.lib.mocks.rabbitmq.rmq_context import RmqContext


class MessageConsumer(Thread):
    def __init__(self, connection_params: pika.ConnectionParameters, rmq_context: RmqContext):
        super().__init__()
        self.__connection_params = connection_params
        self.__rmq_context = rmq_context

        connection = pika.BlockingConnection(self.__connection_params)
        self.channel: BlockingChannel = connection.channel()

    def run(self) -> None:
        super().run()
        self.channel.start_consuming()

    def consume(self, exchange: str, routing_key: str, queue: str):
        def message_received(channel: BlockingChannel, method: spec.Basic.Deliver, properties: spec.BasicProperties,
                             body: bytes):
            payload = str(body, encoding='utf-8')
            self.__rmq_context.track_payload(exchange, routing_key, payload)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue, message_received)


class RabbitmqSetup(object):
    def __init__(self, channel: BlockingChannel, connection_params: pika.ConnectionParameters, rmq_context: RmqContext,
                 durable=False):
        super().__init__()
        self.__channel = channel
        self.__rmq_context = rmq_context
        self.__durable = durable

        self.__message_consumer: MessageConsumer = MessageConsumer(connection_params, rmq_context)
        self.__exchanges: list = []
        self.__queues: list = []

    def load_defaults(self, defaults: dict):
        for queue in self.__queues:
            self.__channel.queue_purge(queue)
        self.__rmq_context.clear()

        for exchange in defaults['exchanges']:
            self.__create_exchange(exchange['name'], exchange['type'])
            for queue in exchange['queues']:
                routing_key = queue.get('routingKey', '')
                self.__create_queue(queue['name'], exchange['name'], routing_key)
        if not self.__message_consumer.is_alive():
            self.__message_consumer.start()

    def stop_listening(self):
        def callback():
            self.__message_consumer.channel.stop_consuming()

        if self.__message_consumer.is_alive():
            self.__message_consumer.channel.connection.add_callback_threadsafe(callback)
            self.__message_consumer.join()

    def publish(self, exchange: str, payload: str, routing_key: str = ''):
        """Publish a message with a payload to the given exchange and optional routing-key."""
        if self.__rmq_context.exchange_is_tracked(exchange, routing_key):
            self.__channel.basic_publish(exchange, routing_key, bytes(payload, encoding='utf-8'))

    def __create_exchange(self, name: str, exchange_type: str = 'direct'):
        if name not in self.__exchanges:
            self.__channel.exchange_declare(name, exchange_type=exchange_type, durable=self.__durable)
            self.__exchanges.append(name)

    def __create_queue(self, name: str, exchange: str, routing_key: str = ''):
        if name not in self.__queues:
            self.__channel.queue_declare(name, durable=self.__durable)
            self.__channel.queue_bind(name, exchange, routing_key=routing_key)
            self.__queues.append(name)

            shadow_queue_name = name + '.touchstone-shadow'
            self.__channel.queue_declare(shadow_queue_name)
            self.__channel.queue_bind(shadow_queue_name, exchange, routing_key=routing_key)
            self.__queues.append(shadow_queue_name)
            self.__rmq_context.track(exchange, routing_key)
            self.__message_consumer.consume(exchange, routing_key, shadow_queue_name)
