from pika.adapters.blocking_connection import BlockingChannel

from touchstone.lib.mocks.mock_case import Exercise


class RabbitmqExercise(Exercise):
    def __init__(self, channel: BlockingChannel):
        super().__init__()
        self.channel: BlockingChannel = channel

    def publish(self, exchange: str, payload: str, routing_key: str = ''):
        self.channel.basic_publish(exchange, routing_key, bytes(payload, encoding='utf8'))
