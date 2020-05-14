from touchstone.lib.touchstone_test import TouchstoneTest


class MessagesPublished(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        return None

    def when(self, given) -> object:
        self.mocks.rabbitmq.setup().publish('default-direct.exchange', 'some payload')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.rabbitmq.verify().messages_published('default-direct.exchange')


class MessagesPublishedWithTimes(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        return None

    def when(self, given) -> object:
        self.mocks.rabbitmq.setup().publish('default-direct.exchange', 'some payload', routing_key='foo')
        self.mocks.rabbitmq.setup().publish('default-direct.exchange', 'some payload', routing_key='foo')
        self.mocks.rabbitmq.setup().publish('default-direct.exchange', 'some payload', routing_key='foo')
        self.mocks.rabbitmq.setup().publish('default-direct.exchange', 'some payload', routing_key='bar')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.rabbitmq.verify().messages_published('default-direct.exchange', num_expected=3,
                                                               routing_key='foo')


class PayloadPublished(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        return 'some payload'

    def when(self, given) -> object:
        self.mocks.rabbitmq.setup().publish('default-topic.exchange', given, routing_key='foo')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.rabbitmq.verify().payload_published('default-topic.exchange', given, routing_key='foo')
