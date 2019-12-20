from touchstone.lib.touchstone_test import TouchstoneTest


class Listen(TouchstoneTest):
    def given(self):
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload', 'foo')

    def when(self):
        pass

    def then(self, test_result) -> bool:
        pass
