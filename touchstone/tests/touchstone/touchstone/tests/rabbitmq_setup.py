from touchstone.lib.touchstone_test import TouchstoneTest


class Listen(TouchstoneTest):
    def given(self):
        pass
        # self.mocks.rabbit_mq.setup().create_exchange('foo')
        # self.mocks.rabbit_mq.setup().create_queue('bar', 'foo')

    def when(self):
        pass

    def then(self, test_result) -> bool:
        pass
