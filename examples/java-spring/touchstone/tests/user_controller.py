from touchstone.lib.touchstone_test import TouchstoneTest


class UserController(TouchstoneTest):
    def given(self):
        pass

    def when(self):
        self.mocks.rabbit_mq.exercise().publish('default-direct.exchange', 'some payload')

    def then(self, test_result) -> bool:
        return self.mocks.rabbit_mq.verify().messages_published('default-direct.exchange')
