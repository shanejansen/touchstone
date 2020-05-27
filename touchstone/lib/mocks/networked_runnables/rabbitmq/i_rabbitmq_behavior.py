import abc


class IRabbitmqSetup(object):
    def publish(self, exchange: str, payload: str, routing_key: str = ''):
        """Publish a message with a payload to the given exchange and optional routing-key."""
        pass


class IRabbitmqVerify(object):
    @abc.abstractmethod
    def messages_published(self, exchange: str, num_expected: int = 1, routing_key: str = '') -> bool:
        """Returns True if messages have been published the given number of times to the given exchange and
        routing-key. If num_expected is set to None, any number of messages will be considered passing."""
        pass

    @abc.abstractmethod
    def payload_published(self, exchange: str, expected_payload: str, routing_key: str = '') -> bool:
        """Returns True if a message with the given payload has been published to the given exchange and routing key."""
        pass


class IRabbitmqBehavior(object):
    DEFAULT_CONFIG = {
        'autoCreate': True
    }

    @abc.abstractmethod
    def setup(self) -> IRabbitmqSetup:
        pass

    @abc.abstractmethod
    def verify(self) -> IRabbitmqVerify:
        pass
