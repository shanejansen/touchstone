from pika.adapters.blocking_connection import BlockingChannel

from touchstone.lib.mocks.mock_case import Verify
from touchstone.lib.mocks.rabbitmq.rmq_context import RmqContext


class RabbitmqVerify(Verify):
    def __init__(self, channel: BlockingChannel, rmq_context: RmqContext):
        super().__init__()
        self.__channel: BlockingChannel = channel
        self.__rmq_context = rmq_context

    def messages_published(self, exchange: str, times: int = None, routing_key: str = '') -> bool:
        """Returns True if a messages has been published the given number of times to the given exchange and routing_
        key. If times is not supplied, any number of messages will be considered passing."""
        num_messages = self.__rmq_context.messages_published(exchange, routing_key)
        if not times and num_messages != 0:
            return True
        return self.expected_matches_actual(num_messages, times)

    def payload_published(self, exchange: str, expected_payload: str, routing_key: str = '') -> bool:
        """Returns True if a message with the given payload has been published to the given exchange and routing key."""
        payloads = self.__rmq_context.payloads_published(exchange, routing_key)
        return self.expected_in_actual(expected_payload, payloads)
