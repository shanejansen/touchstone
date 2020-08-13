from touchstone.helpers import http
from touchstone.lib.touchstone_test import TouchstoneTest


class Get(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup().get('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.get(f'{self.mocks.http.url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify().get_called('/some-endpoint')


class GetWithTimes(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup().get('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.get(f'{self.mocks.http.url()}/some-endpoint')
        http.get(f'{self.mocks.http.url()}/some-endpoint')
        http.get(f'{self.mocks.http.url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify().get_called('/some-endpoint', times=3)


class Post(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup().post('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.post(f'{self.mocks.http.url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify().post_called('/some-endpoint')


class Put(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup().put('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.put(f'{self.mocks.http.url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify().put_called('/some-endpoint')


class Delete(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup().delete('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.delete(f'{self.mocks.http.url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify().delete_called('/some-endpoint')


class PostContained(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup().post('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.post(f'{self.mocks.http.url()}/some-endpoint', 'foo')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify().post_contained('/some-endpoint', 'foo')


class PutContained(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup().put('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.put(f'{self.mocks.http.url()}/some-endpoint', 'foo')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify().put_contained('/some-endpoint', 'foo')


class DeleteContained(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup().delete('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.delete(f'{self.mocks.http.url()}/some-endpoint', 'foo')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify().delete_contained('/some-endpoint', 'foo')


class WildcardMatches(TouchstoneTest):
    def given(self) -> object:
        self.mocks.http.setup().get('/some-endpoint/([a-z]*)/bar', 'hello http!')
        return None

    def when(self, given) -> object:
        http.get(f'{self.mocks.http.url()}/some-endpoint/foo/bar')
        return None

    def then(self, given, result) -> bool:
        return self.mocks.http.verify().get_called('/some-endpoint/foo/bar')
