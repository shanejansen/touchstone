from touchstone.lib.touchstone_test import TouchstoneTest


class MessagesPublished(TouchstoneTest):
    def given(self):
        pass

    def when(self):
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload')

    def then(self, test_result) -> bool:
        return self.mocks.rabbit_mq.verify().messages_published('default-direct.exchange')


class MessagesPublishedWithTimes(TouchstoneTest):
    def given(self):
        pass

    def when(self):
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload', routing_key='foo')
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload', routing_key='foo')
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload', routing_key='foo')
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload', routing_key='bar')

    def then(self, test_result) -> bool:
        return self.mocks.rabbit_mq.verify().messages_published('default-direct.exchange', num_expected_messages=3,
                                                                routing_key='foo')


class PayloadPublished(TouchstoneTest):
    def given(self):
        pass

    def when(self):
        self.mocks.rabbit_mq.exercise().publish('default-topic.exchange', 'some payload', routing_key='foo')

    def then(self, test_result) -> bool:
        return self.mocks.rabbit_mq.verify().payload_published('default-topic.exchange', 'some payload',
                                                               routing_key='foo')
