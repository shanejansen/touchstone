from pika.adapters.blocking_connection import BlockingChannel

from touchstone.lib.mocks.rabbitmq.rmq_context import RmqContext


class RabbitmqExercise(object):
    def __init__(self, channel: BlockingChannel, rmq_context: RmqContext):
        super().__init__()
        self.__channel: BlockingChannel = channel
        self.__rmq_context = rmq_context

    def publish(self, exchange: str, payload: str, routing_key: str = ''):
        if self.__rmq_context.exchange_is_tracked(exchange, routing_key):
            self.__channel.basic_publish(exchange, routing_key, bytes(payload, encoding='utf-8'))
