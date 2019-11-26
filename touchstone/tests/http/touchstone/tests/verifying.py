import urllib.request

from touchstone.lib.touchstone_test import TouchstoneTest


class GetCalled(TouchstoneTest):
    def given(self):
        self.mocks.http.setup().get('/some-endpoint', 'hello http!')

    def when(self):
        urllib.request.urlopen('http://localhost:8085/some-endpoint')

    def then(self, test_result) -> bool:
        return self.mocks.http.verify().get_called('/some-endpoint')


class GetCalledWithTimes(TouchstoneTest):
    def given(self):
        self.mocks.http.setup().get('/some-endpoint', 'hello http!')

    def when(self):
        urllib.request.urlopen('http://localhost:8085/some-endpoint')
        urllib.request.urlopen('http://localhost:8085/some-endpoint')
        urllib.request.urlopen('http://localhost:8085/some-endpoint')

    def then(self, test_result) -> bool:
        expected_calls = 3
        return self.mocks.http.verify().get_called('/some-endpoint', times=expected_calls)


class PostCalled(TouchstoneTest):
    def given(self):
        self.mocks.http.setup().post('/some-endpoint', 'hello http!')

    def when(self):
        urllib.request.urlopen('http://localhost:8085/some-endpoint', data=[])

    def then(self, test_result) -> bool:
        return self.mocks.http.verify().post_called('/some-endpoint')


class PutCalled(TouchstoneTest):
    def given(self):
        self.mocks.http.setup().put('/some-endpoint', 'hello http!')

    def when(self):
        request = urllib.request.Request('http://localhost:8085/some-endpoint', method='PUT')
        urllib.request.urlopen(request)

    def then(self, test_result) -> bool:
        return self.mocks.http.verify().put_called('/some-endpoint')


class DeleteCalled(TouchstoneTest):
    def given(self):
        self.mocks.http.setup().delete('/some-endpoint', 'hello http!')

    def when(self):
        request = urllib.request.Request('http://localhost:8085/some-endpoint', method='DELETE')
        urllib.request.urlopen(request)

    def then(self, test_result) -> bool:
        return self.mocks.http.verify().delete_called('/some-endpoint')


class PostContained(TouchstoneTest):
    def given(self):
        pass

    def when(self):
        pass

    def then(self, test_result) -> bool:
        return True
