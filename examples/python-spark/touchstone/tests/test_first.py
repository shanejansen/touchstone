from touchstone.lib.touchstone_test import TouchstoneTest


class First(TouchstoneTest):
    def given(self) -> object:
        pass

    def when(self, given) -> object:
        self.service_executor.execute('my-exec')

    def then(self, given, result) -> bool:
        pass
