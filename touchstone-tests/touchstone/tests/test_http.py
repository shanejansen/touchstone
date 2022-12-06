import json

from touchstone.helpers import http
from touchstone.lib.touchstone_test import TouchstoneTest


class Get(TouchstoneTest):
    def given(self) -> object:
        self.deps.http.setup().get('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.get(f'{self.deps.http.url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        return self.deps.http.verify().get_called('/some-endpoint')


class GetWithTimes(TouchstoneTest):
    def given(self) -> object:
        self.deps.http.setup().get('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.get(f'{self.deps.http.url()}/some-endpoint')
        http.get(f'{self.deps.http.url()}/some-endpoint')
        http.get(f'{self.deps.http.url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        return self.deps.http.verify().get_called('/some-endpoint', times=3)


class GetWithTimesZero(TouchstoneTest):
    def given(self) -> object:
        self.deps.http.setup().get('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        return None

    def then(self, given, result) -> bool:
        return self.deps.http.verify().get_called('/some-endpoint', times=0)


class Post(TouchstoneTest):
    def given(self) -> object:
        self.deps.http.setup().post('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.post(f'{self.deps.http.url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        return self.deps.http.verify().post_called('/some-endpoint')


class PostContained(TouchstoneTest):
    def given(self) -> object:
        self.deps.http.setup().post('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.post(f'{self.deps.http.url()}/some-endpoint', 'foo')
        return None

    def then(self, given, result) -> bool:
        return self.deps.http.verify().post_contained('/some-endpoint', 'foo')


class PostContainedJson(TouchstoneTest):
    def given(self) -> object:
        given = {'foo': 'bar'}
        self.deps.http.setup().post('/some-endpoint', 'hello http!')
        return given

    def when(self, given) -> object:
        http.post(f'{self.deps.http.url()}/some-endpoint', json.dumps(given))
        return None

    def then(self, given, result) -> bool:
        return self.deps.http.verify().post_contained_json('/some-endpoint', given)


class Put(TouchstoneTest):
    def given(self) -> object:
        self.deps.http.setup().put('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.put(f'{self.deps.http.url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        return self.deps.http.verify().put_called('/some-endpoint')


class Delete(TouchstoneTest):
    def given(self) -> object:
        self.deps.http.setup().delete('/some-endpoint', 'hello http!')
        return None

    def when(self, given) -> object:
        http.delete(f'{self.deps.http.url()}/some-endpoint')
        return None

    def then(self, given, result) -> bool:
        return self.deps.http.verify().delete_called('/some-endpoint')


class WildcardMatches(TouchstoneTest):
    def given(self) -> object:
        self.deps.http.setup().get('/some-endpoint/([a-z]*)/bar', 'hello http!', url_pattern=True)
        return None

    def when(self, given) -> object:
        http.get(f'{self.deps.http.url()}/some-endpoint/foo/bar')
        return None

    def then(self, given, result) -> bool:
        return self.deps.http.verify().get_called('/some-endpoint/([a-z]*)/bar', url_pattern=True)
