import urllib.request

from touchstone.lib.touchstone_test import TouchstoneTest


class GetCalled(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup.get('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        urllib.request.urlopen(f'{self.mocks.http.default_url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify.get_called('/some-endpoint')


class GetCalledWithTimes(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup.get('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        urllib.request.urlopen(f'{self.mocks.http.default_url()}/some-endpoint')
        urllib.request.urlopen(f'{self.mocks.http.default_url()}/some-endpoint')
        urllib.request.urlopen(f'{self.mocks.http.default_url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        expected_calls = 3
        return self.mocks.http.verify.get_called('/some-endpoint', times=expected_calls)


class PostCalled(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup.post('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        urllib.request.urlopen(f'{self.mocks.http.default_url()}/some-endpoint', data=bytes())
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify.post_called('/some-endpoint')


class PutCalled(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup.put('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        request = urllib.request.Request(f'{self.mocks.http.default_url()}/some-endpoint', method='PUT')
        urllib.request.urlopen(request)
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify.put_called('/some-endpoint')


class DeleteCalled(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup.delete('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        request = urllib.request.Request(f'{self.mocks.http.default_url()}/some-endpoint', method='DELETE')
        urllib.request.urlopen(request)
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify.delete_called('/some-endpoint')


class PostContained(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup.post('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        body = 'foo'.encode('utf8')
        request = urllib.request.Request(f'{self.mocks.http.default_url()}/some-endpoint', method='POST', data=body)
        urllib.request.urlopen(request)
        return None

    def then(self, given, result) -> bool:
        expected_body = 'foo'
        return self.mocks.http.verify.post_contained('/some-endpoint', expected_body)


class PutContained(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup.put('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        body = 'foo'.encode('utf8')
        request = urllib.request.Request(f'{self.mocks.http.default_url()}/some-endpoint', method='PUT', data=body)
        urllib.request.urlopen(request)
        return None

    def then(self, given, result) -> bool:
        expected_body = 'foo'
        return self.mocks.http.verify.put_contained('/some-endpoint', expected_body)


class DeleteContained(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup.delete('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        body = 'foo'.encode('utf8')
        request = urllib.request.Request(f'{self.mocks.http.default_url()}/some-endpoint', method='DELETE', data=body)
        urllib.request.urlopen(request)
        return None

    def then(self, given, result) -> bool:
        expected_body = 'foo'
        return self.mocks.http.verify.delete_contained('/some-endpoint', expected_body)
