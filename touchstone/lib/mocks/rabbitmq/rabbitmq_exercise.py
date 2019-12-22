import time
from pika.adapters.blocking_connection import BlockingChannel

from touchstone.lib.mocks.mock_case import Exercise


class RabbitmqExercise(Exercise):
    def __init__(self, channel: BlockingChannel, consume_length: float):
        super().__init__()
        self.__channel: BlockingChannel = channel
        self.__consume_length = consume_length

    def publish(self, exchange: str, payload: str, routing_key: str = ''):
        self.__channel.basic_publish(exchange, routing_key, bytes(payload, encoding='utf8'))
        time.sleep(self.__consume_length)
