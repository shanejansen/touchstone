from touchstone.lib.touchstone_test import TouchstoneTest


class MessagesPublished(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self):
        pass

    def when(self):
        self.mocks.rabbitmq.setup.publish('default-direct.exchange', 'some payload')

    def then(self, test_result) -> bool:
        return self.mocks.rabbitmq.verify.messages_published('default-direct.exchange')


class MessagesPublishedWithTimes(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self):
        pass

    def when(self):
        self.mocks.rabbitmq.setup.publish('default-direct.exchange', 'some payload', routing_key='foo')
        self.mocks.rabbitmq.setup.publish('default-direct.exchange', 'some payload', routing_key='foo')
        self.mocks.rabbitmq.setup.publish('default-direct.exchange', 'some payload', routing_key='foo')
        self.mocks.rabbitmq.setup.publish('default-direct.exchange', 'some payload', routing_key='bar')

    def then(self, test_result) -> bool:
        return self.mocks.rabbitmq.verify.messages_published('default-direct.exchange', num_expected=3,
                                                             routing_key='foo')


class PayloadPublished(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self):
        pass

    def when(self):
        self.mocks.rabbitmq.setup.publish('default-topic.exchange', 'some payload', routing_key='foo')

    def then(self, test_result) -> bool:
        return self.mocks.rabbitmq.verify.payload_published('default-topic.exchange', 'some payload',
                                                            routing_key='foo')
