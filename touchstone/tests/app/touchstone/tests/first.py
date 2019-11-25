import json

from touchstone.lib.touchstone_test import TouchstoneTest


class HttpMocking(TouchstoneTest):
    def given(self):
        response = {
            'foo': 'bar'
        }
        self.mocks.http.setup().get('/foo', json.dumps(response))

    def when(self):
        return 1

    def then(self, test_result) -> bool:
        return test_result == 1


class AnotherOne(TouchstoneTest):
    def given(self):
        pass

    def when(self):
        pass

    def then(self, test_result) -> bool:
        return True
