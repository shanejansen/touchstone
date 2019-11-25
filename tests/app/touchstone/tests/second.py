from touchstone_test import TouchstoneTest


class ThisShouldPass(TouchstoneTest):
    def given(self):
        pass

    def when(self):
        return 'bar'

    def then(self, test_result) -> bool:
        return test_result is 'bar'
