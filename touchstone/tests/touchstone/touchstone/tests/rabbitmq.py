from touchstone.lib.touchstone_test import TouchstoneTest


class MessagesPublished(TouchstoneTest):
    def given(self):
        pass

    def when(self):
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload', 'foo')

    def then(self, test_result) -> bool:
        return self.mocks.rabbit_mq.verify().messages_published('default-direct.exchange', 'foo')


class MessagesPublishedWithTimes(TouchstoneTest):
    def given(self):
        pass

    def when(self):
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload', 'foo')
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload', 'foo')
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload', 'foo')
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload', 'bar')

    def then(self, test_result) -> bool:
        return self.mocks.rabbit_mq.verify().messages_published('default-direct.exchange', 'foo', times=3)
