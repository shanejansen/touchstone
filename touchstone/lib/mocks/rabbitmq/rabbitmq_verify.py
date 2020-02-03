from pika.adapters.blocking_connection import BlockingChannel

from touchstone.lib.mocks import validation
from touchstone.lib.mocks.rabbitmq.rmq_context import RmqContext


class RabbitmqVerify(object):
    def __init__(self, channel: BlockingChannel, rmq_context: RmqContext):
        super().__init__()
        self.__channel: BlockingChannel = channel
        self.__rmq_context = rmq_context

    def messages_published(self, exchange: str, num_expected: int = 1, routing_key: str = '') -> bool:
        """Returns True if messages have been published the given number of times to the given exchange and
        routing-key. If num_expected is set to None, any number of messages will be considered passing."""
        if not self.__rmq_context.exchange_is_tracked(exchange, routing_key):
            return False
        num_messages = self.__rmq_context.messages_published(exchange, routing_key)
        if not num_expected and num_messages != 0:
            return True
        return validation.matches(num_expected, num_messages)

    def payload_published(self, exchange: str, expected_payload: str, routing_key: str = '') -> bool:
        """Returns True if a message with the given payload has been published to the given exchange and routing key."""
        if not self.__rmq_context.exchange_is_tracked(exchange, routing_key):
            return False
        payloads = self.__rmq_context.payloads_published(exchange, routing_key)
        return validation.contains(expected_payload, payloads)
