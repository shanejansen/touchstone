import time

from pika.adapters.blocking_connection import BlockingChannel

from touchstone.lib.mocks.mock_case import Exercise
from touchstone.lib.mocks.rabbitmq.rmq_context import RmqContext


class RabbitmqExercise(Exercise):
    def __init__(self, channel: BlockingChannel, rmq_context: RmqContext, consume_length: float):
        super().__init__()
        self.__channel: BlockingChannel = channel
        self.__rmq_context = rmq_context
        self.__consume_length = consume_length

    def publish(self, exchange: str, payload: str, routing_key: str = ''):
        if not self.__rmq_context.exchange_is_tracked(exchange, routing_key):
            print('This exchange/routing-key combination is not defined. Check your "rabbitmq.yml" defaults.')
        else:
            self.__channel.basic_publish(exchange, routing_key, bytes(payload, encoding='utf-8'))
            time.sleep(self.__consume_length)
