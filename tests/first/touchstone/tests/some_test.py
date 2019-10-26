from touchstone_test import TouchstoneTest


class SomeTest(TouchstoneTest):
    def name(self):
        return 'Some Test'

    def given(self, given_context):
        pass

    def when(self, when_context):
        return 1

    def then(self, then_context, test_result):
        return test_result == 1
