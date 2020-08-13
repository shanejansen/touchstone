import json
from threading import Thread

import pika
import pika.exceptions
from pika import spec, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel

from touchstone.lib.mocks.networked_runnables.rabbitmq.docker.docker_rabbitmq_context import DockerRabbitmqContext
from touchstone.lib.mocks.networked_runnables.rabbitmq.i_rabbitmq_behavior import IRabbitmqSetup


class MessageConsumer(Thread):
    def __init__(self, connection_params: pika.ConnectionParameters, rmq_context: DockerRabbitmqContext):
        super().__init__()
        self.__connection_params = connection_params
        self.__rmq_context = rmq_context

        connection = pika.BlockingConnection(self.__connection_params)
        self.channel: BlockingChannel = connection.channel()

    def run(self) -> None:
        super().run()
        try:
            self.channel.start_consuming()
        except pika.exceptions.ConnectionClosedByBroker:
            pass

    def consume(self, exchange: str, routing_key: str, queue: str):
        def message_received(channel: BlockingChannel, method: spec.Basic.Deliver, properties: spec.BasicProperties,
                             body: bytes):
            payload = str(body, encoding='utf-8')
            self.__rmq_context.track_payload(exchange, routing_key, payload)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue, message_received)


class DockerRabbitmqSetup(IRabbitmqSetup):
    def __init__(self, rmq_context: DockerRabbitmqContext):
        super().__init__()
        self.__rmq_context = rmq_context
        self.__channel = None
        self.__message_consumer = None
        self.__exchanges: list = []
        self.__queues: list = []
        self.__shadow_queues: list = []

    def set_channel(self, channel: BlockingChannel):
        self.__channel = channel

    def set_connection_params(self, connection_params: pika.ConnectionParameters):
        self.__message_consumer = MessageConsumer(connection_params, self.__rmq_context)

    def purge_queues(self):
        for queue in self.__queues:
            self.__channel.queue_purge(queue)
        for queue in self.__shadow_queues:
            self.__channel.queue_purge(queue)
        self.__rmq_context.clear()

    def create_all(self, defaults: dict):
        for exchange in defaults.get('exchanges', []):
            self.__create_exchange(exchange['name'], exchange['type'])
            for queue in exchange.get('queues', []):
                routing_key = queue.get('routingKey', '')
                self.__create_queue(queue['name'], exchange['name'], routing_key)
                self.__create_shadow_queue(queue['name'], exchange['name'], routing_key)
        if not self.__message_consumer.is_alive():
            self.__message_consumer.start()

    def create_shadow_queues(self, defaults: dict):
        for exchange in defaults.get('exchanges', []):
            for queue in exchange.get('queues', []):
                routing_key = queue.get('routingKey', '')
                self.__create_shadow_queue(queue['name'], exchange['name'], routing_key)
        if not self.__message_consumer.is_alive():
            self.__message_consumer.start()

    def stop_listening(self):
        def callback():
            self.__message_consumer.channel.stop_consuming()

        if self.__message_consumer and self.__message_consumer.is_alive():
            self.__message_consumer.channel.connection.add_callback_threadsafe(callback)
            self.__message_consumer.join()

    def publish(self, exchange: str, payload: str, routing_key: str = '', content_type: str = None,
                headers: dict = None):
        if self.__rmq_context.exchange_is_tracked(exchange, routing_key):
            properties = BasicProperties(content_type=content_type, headers=headers)
            self.__channel.basic_publish(exchange, routing_key, bytes(payload, encoding='utf-8'), properties=properties)

    def publish_json(self, exchange: str, payload: dict, routing_key: str = '', headers: dict = None):
        self.publish(exchange, json.dumps(payload), routing_key, 'application/json', headers)

    def __create_exchange(self, name: str, exchange_type: str = 'direct'):
        if name not in self.__exchanges:
            self.__channel.exchange_declare(name, exchange_type=exchange_type)
            self.__exchanges.append(name)

    def __create_queue(self, name: str, exchange: str, routing_key: str = ''):
        if name not in self.__queues:
            self.__channel.queue_declare(name)
            self.__channel.queue_bind(name, exchange, routing_key=routing_key)
            self.__queues.append(name)

    def __create_shadow_queue(self, name: str, exchange: str, routing_key: str = ''):
        name = name + '.ts-shadow'
        if name not in self.__shadow_queues:
            self.__channel.queue_declare(name)
            self.__channel.queue_bind(name, exchange, routing_key=routing_key)
            self.__shadow_queues.append(name)
            self.__rmq_context.track(exchange, routing_key)
            self.__message_consumer.consume(exchange, routing_key, name)
