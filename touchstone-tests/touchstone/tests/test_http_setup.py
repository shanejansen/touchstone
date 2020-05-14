import json
import urllib.request

from touchstone.lib.mocks import validation
from touchstone.lib.touchstone_test import TouchstoneTest


class Get(TouchstoneTest):
    def given(self) -> object:
        given = json.dumps({'foo': 'get'})
        self.mocks.http.setup().get('/get-endpoint', given)
        return given

    def when(self, given) -> object:
        response = urllib.request.urlopen(f'{self.mocks.http.url()}/get-endpoint').read()
        return response.decode('utf-8')

    def then(self, given, result) -> bool:
        return validation.matches(given, result)


class Post(TouchstoneTest):
    def given(self) -> object:
        given = json.dumps({'foo': 'post'})
        self.mocks.http.setup().post('/post-endpoint', given)
        return given

    def when(self, given) -> object:
        response = urllib.request.urlopen(f'{self.mocks.http.url()}/post-endpoint',
                                          data=bytes()).read()
        return response.decode('utf-8')

    def then(self, given, result) -> bool:
        return validation.matches(given, result)


class Put(TouchstoneTest):
    def given(self) -> object:
        given = json.dumps({'foo': 'put'})
        self.mocks.http.setup().put('/put-endpoint', given)
        return given

    def when(self, given) -> object:
        request = urllib.request.Request(f'{self.mocks.http.url()}/put-endpoint', method='PUT')
        response = urllib.request.urlopen(request).read()
        return response.decode('utf-8')

    def then(self, given, result) -> bool:
        return validation.matches(given, result)


class Delete(TouchstoneTest):
    def given(self) -> object:
        given = json.dumps({'foo': 'delete'})
        self.mocks.http.setup().delete('/delete-endpoint', given)
        return given

    def when(self, given) -> object:
        request = urllib.request.Request(f'{self.mocks.http.url()}/delete-endpoint', method='DELETE')
        response = urllib.request.urlopen(request).read()
        return response.decode('utf-8')

    def then(self, given, result) -> bool:
        return validation.matches(given, result)
