import json
import urllib.request

from touchstone.lib.touchstone_test import TouchstoneTest


class Get(TouchstoneTest):
    def given(self):
        response = {
            'foo': 'get'
        }
        self.mocks.http.setup().get('/get-endpoint', json.dumps(response))

    def when(self):
        response = urllib.request.urlopen('http://localhost:8085/get-endpoint').read()
        return response.decode("utf-8")

    def then(self, test_result) -> bool:
        expected_response = {
            'foo': 'get'
        }
        return test_result == json.dumps(expected_response)


class Post(TouchstoneTest):
    def given(self):
        response = {
            'foo': 'post'
        }
        self.mocks.http.setup().post('/post-endpoint', json.dumps(response))

    def when(self):
        response = urllib.request.urlopen('http://localhost:8085/post-endpoint', data=[]).read()
        return response.decode("utf-8")

    def then(self, test_result) -> bool:
        expected_response = {
            'foo': 'post'
        }
        return test_result == json.dumps(expected_response)


class Put(TouchstoneTest):
    def given(self):
        response = {
            'foo': 'put'
        }
        self.mocks.http.setup().put('/put-endpoint', json.dumps(response))

    def when(self):
        request = urllib.request.Request('http://localhost:8085/put-endpoint', method='PUT')
        response = urllib.request.urlopen(request).read()
        return response.decode("utf-8")

    def then(self, test_result) -> bool:
        expected_response = {
            'foo': 'put'
        }
        return test_result == json.dumps(expected_response)


class Delete(TouchstoneTest):
    def given(self):
        response = {
            'foo': 'delete'
        }
        self.mocks.http.setup().delete('/delete-endpoint', json.dumps(response))

    def when(self):
        request = urllib.request.Request('http://localhost:8085/delete-endpoint', method='DELETE')
        response = urllib.request.urlopen(request).read()
        return response.decode("utf-8")

    def then(self, test_result) -> bool:
        expected_response = {
            'foo': 'delete'
        }
        return test_result == json.dumps(expected_response)
