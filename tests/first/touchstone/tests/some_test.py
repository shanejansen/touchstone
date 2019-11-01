import json

from touchstone_test import TouchstoneTest


class SomeTest(TouchstoneTest):
    def name(self):
        return 'Some Test'

    def given(self, given_context):
        response = {
            'foo': 'bar'
        }
        given_context.mocks.http.mock_get('/foo', json.dumps(response))

    def when(self, when_context):
        return 1

    def then(self, then_context, test_result):
        return test_result == 1
