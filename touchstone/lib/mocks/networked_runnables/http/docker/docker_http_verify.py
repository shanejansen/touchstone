import json
import urllib.request
from json.decoder import JSONDecodeError

from touchstone.helpers import validation
from touchstone.lib.mocks.networked_runnables.http.i_http_behavior import IHttpVerify


class DockerHttpVerify(IHttpVerify):
    def __init__(self):
        super().__init__()
        self.__url = None

    def set_url(self, url: str):
        self.__url = url

    def get_called(self, endpoint: str, times: int = 1) -> bool:
        return self.__count_verification(endpoint, 'GET', times)

    def post_called(self, endpoint: str, times: int = 1) -> bool:
        return self.__count_verification(endpoint, 'POST', times)

    def post_contained(self, endpoint: str, expected_body: str) -> bool:
        return self.__contained_verification(endpoint, 'POST', expected_body)

    def post_contained_json(self, endpoint: str, expected_body: dict) -> bool:
        return self.__contained_json_verification(endpoint, 'POST', expected_body)

    def put_called(self, endpoint: str, times: int = 1) -> bool:
        return self.__count_verification(endpoint, 'PUT', times)

    def put_contained(self, endpoint: str, expected_body: str) -> bool:
        return self.__contained_verification(endpoint, 'PUT', expected_body)

    def put_contained_json(self, endpoint: str, expected_body: dict) -> bool:
        return self.__contained_json_verification(endpoint, 'PUT', expected_body)

    def delete_called(self, endpoint: str, times: int = 1) -> bool:
        return self.__count_verification(endpoint, 'DELETE', times)

    def delete_contained(self, endpoint: str, expected_body: str) -> bool:
        return self.__contained_verification(endpoint, 'DELETE', expected_body)

    def delete_contained_json(self, endpoint: str, expected_body: dict) -> bool:
        return self.__contained_json_verification(endpoint, 'DELETE', expected_body)

    def __count_verification(self, endpoint, http_verb, times):
        payload = {
            'method': http_verb,
            'url': endpoint
        }
        data = json.dumps(payload).encode('utf-8')
        request = urllib.request.Request(
            f'{self.__url}/__admin/requests/count',
            data=data,
            headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        call_count = json.loads(response)['count']
        if times is None:
            return call_count > 0
        return validation.matches(times, call_count)

    def __get_request_bodies(self, endpoint, http_verb):
        payload = {
            'method': http_verb,
            'url': endpoint
        }
        data = json.dumps(payload).encode('utf-8')
        request = urllib.request.Request(
            f'{self.__url}/__admin/requests/find',
            data=data,
            headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        bodies = []
        for request in json.loads(response)['requests']:
            bodies.append(request['body'])
        return bodies

    def __contained_verification(self, endpoint, http_verb, expected_body):
        bodies = self.__get_request_bodies(endpoint, http_verb)
        return validation.contains(expected_body, bodies)

    def __contained_json_verification(self, endpoint, http_verb, expected_body):
        bodies = self.__get_request_bodies(endpoint, http_verb)
        for body in bodies:
            try:
                body = json.loads(body)
                if validation.matches(expected_body, body, quiet=True):
                    return True
            except JSONDecodeError:
                pass
        print(f'Expected:\n{expected_body}\nwas not found in actual:\n{bodies}')
        return False
