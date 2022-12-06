import json
import urllib.request
from json.decoder import JSONDecodeError

from touchstone.helpers import validation
from touchstone.lib.nodes.deps.behaviors.i_http_behavior import IHttpVerify


class DockerHttpVerify(IHttpVerify):
    def __init__(self):
        super().__init__()
        self.__url = None

    def set_url(self, url: str):
        self.__url = url

    def get_called(self, endpoint: str, times: int = 1, url_pattern: bool = False) -> bool:
        return self.__count_verification(endpoint, 'GET', times, url_pattern)

    def post_called(self, endpoint: str, times: int = 1, url_pattern: bool = False) -> bool:
        return self.__count_verification(endpoint, 'POST', times, url_pattern)

    def post_contained(self, endpoint: str, expected_body: str, url_pattern: bool = False) -> bool:
        return self.__contained_verification(endpoint, 'POST', expected_body, url_pattern)

    def post_contained_json(self, endpoint: str, expected_body: dict, url_pattern: bool = False) -> bool:
        return self.__contained_json_verification(endpoint, 'POST', expected_body, url_pattern)

    def put_called(self, endpoint: str, times: int = 1, url_pattern: bool = False) -> bool:
        return self.__count_verification(endpoint, 'PUT', times, url_pattern)

    def put_contained(self, endpoint: str, expected_body: str, url_pattern: bool = False) -> bool:
        return self.__contained_verification(endpoint, 'PUT', expected_body, url_pattern)

    def put_contained_json(self, endpoint: str, expected_body: dict, url_pattern: bool = False) -> bool:
        return self.__contained_json_verification(endpoint, 'PUT', expected_body, url_pattern)

    def delete_called(self, endpoint: str, times: int = 1, url_pattern: bool = False) -> bool:
        return self.__count_verification(endpoint, 'DELETE', times, url_pattern)

    def delete_contained(self, endpoint: str, expected_body: str, url_pattern: bool = False) -> bool:
        return self.__contained_verification(endpoint, 'DELETE', expected_body, url_pattern)

    def delete_contained_json(self, endpoint: str, expected_body: dict, url_pattern: bool = False) -> bool:
        return self.__contained_json_verification(endpoint, 'DELETE', expected_body, url_pattern)

    def __count_verification(self, endpoint, http_verb, times, url_pattern):
        payload = {
            'method': http_verb,
            self.__get_url_type(url_pattern): endpoint
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

    def __get_request_bodies(self, endpoint, http_verb, url_pattern):
        payload = {
            'method': http_verb,
            self.__get_url_type(url_pattern): endpoint
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

    def __get_url_type(self, url_pattern: bool):
        if url_pattern:
            return 'urlPattern'
        return 'url'

    def __contained_verification(self, endpoint, http_verb, expected_body, url_pattern):
        bodies = self.__get_request_bodies(endpoint, http_verb, url_pattern)
        return validation.contains(expected_body, bodies)

    def __contained_json_verification(self, endpoint, http_verb, expected_body, url_pattern):
        bodies = self.__get_request_bodies(endpoint, http_verb, url_pattern)
        for body in bodies:
            try:
                body = json.loads(body)
                if validation.matches(expected_body, body, quiet=True):
                    return True
            except JSONDecodeError:
                pass
        print(f'Expected:\n{expected_body}\nwas not found in actual:\n{bodies}')
        return False
