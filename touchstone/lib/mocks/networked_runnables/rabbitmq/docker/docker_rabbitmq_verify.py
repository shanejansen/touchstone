import json
from json.decoder import JSONDecodeError

from pika.adapters.blocking_connection import BlockingChannel

from touchstone.helpers import validation
from touchstone.lib.mocks.networked_runnables.rabbitmq.docker.docker_rabbitmq_context import DockerRabbitmqContext
from touchstone.lib.mocks.networked_runnables.rabbitmq.i_rabbitmq_behavior import IRabbitmqVerify


class DockerRabbitmqVerify(IRabbitmqVerify):
    def __init__(self, rmq_context: DockerRabbitmqContext):
        super().__init__()
        self.__rmq_context = rmq_context
        self.__channel = None

    def set_blocking_channel(self, channel: BlockingChannel):
        self.__channel = channel

    def messages_published(self, exchange: str, num_expected: int = 1, routing_key: str = '') -> bool:
        if not self.__rmq_context.exchange_is_tracked(exchange, routing_key):
            return False
        num_messages = self.__rmq_context.messages_published(exchange, routing_key)
        if not num_expected and num_messages != 0:
            return True
        return validation.matches(num_expected, num_messages)

    def payload_published(self, exchange: str, expected_payload: str, routing_key: str = '') -> bool:
        if not self.__rmq_context.exchange_is_tracked(exchange, routing_key):
            return False
        payloads = self.__rmq_context.payloads_published(exchange, routing_key)
        return validation.contains(expected_payload, payloads)

    def payload_published_json(self, exchange: str, expected_payload: dict, routing_key: str = '') -> bool:
        if not self.__rmq_context.exchange_is_tracked(exchange, routing_key):
            return False
        payloads = self.__rmq_context.payloads_published(exchange, routing_key)
        for payload in payloads:
            try:
                payload = json.loads(payload)
                if validation.matches(expected_payload, payload, quiet=True):
                    return True
            except JSONDecodeError:
                pass
        print(f'Expected:\n{expected_payload}\nwas not found in actual:\n{payloads}')
        return False
