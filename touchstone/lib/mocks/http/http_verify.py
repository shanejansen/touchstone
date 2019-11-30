import json
import urllib.request

from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.mocks.mock_case import Verify


class HttpVerify(Verify):
    def __init__(self, exposed_port: int):
        super().__init__(exposed_port)

    def get_called(self, endpoint: str, times: int = None) -> bool:
        """Returns True if the given endpoint has been called with a GET request the given number of times.
        If times is not supplied, the endpoint can be called any number of times."""
        return self.__count_verification(endpoint, 'GET', times)

    def post_called(self, endpoint: str, times: int = None) -> bool:
        """Returns True if the given endpoint has been called with a POST request the given number of times.
        If times is not supplied, the endpoint can be called any number of times."""
        return self.__count_verification(endpoint, 'POST', times)

    def put_called(self, endpoint: str, times: int = None) -> bool:
        """Returns True if the given endpoint has been called with a PUT request the given number of times.
        If times is not supplied, the endpoint can be called any number of times."""
        return self.__count_verification(endpoint, 'PUT', times)

    def delete_called(self, endpoint: str, times: int = None) -> bool:
        """Returns True if the given endpoint has been called with a DELETE request the given number of times.
        If times is not supplied, the endpoint can be called any number of times."""
        return self.__count_verification(endpoint, 'DELETE', times)

    def post_contained(self, endpoint: str, expected_body: str) -> bool:
        """Returns True if the given endpoint has been called with a POST request containing the given expected
        body."""
        return self.__contained_verification(endpoint, "POST", expected_body)

    def put_contained(self, endpoint: str, expected_body: str) -> bool:
        """Returns True if the given endpoint has been called with a PUT request containing the given expected
        body."""
        return self.__contained_verification(endpoint, "PUT", expected_body)

    def delete_contained(self, endpoint: str, expected_body: str) -> bool:
        """Returns True if the given endpoint has been called with a DELETE request containing the given expected
        body."""
        return self.__contained_verification(endpoint, "DELETE", expected_body)

    def __count_verification(self, endpoint, http_verb, times):
        payload = {
            'method': http_verb,
            'url': endpoint
        }
        data = json.dumps(payload).encode('utf8')
        request = urllib.request.Request(
            f'http://{TouchstoneConfig.instance().config["host"]}:{self.exposed_port}/__admin/requests/count',
            data=data,
            headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        call_count = json.loads(response)['count']
        if not times:
            return call_count > 0
        return self.expected_matches_actual(times, call_count)

    def __contained_verification(self, endpoint, http_verb, expected_body):
        payload = {
            'method': http_verb,
            'url': endpoint
        }
        data = json.dumps(payload).encode('utf8')
        request = urllib.request.Request(
            f'http://{TouchstoneConfig.instance().config["host"]}:{self.exposed_port}/__admin/requests/find',
            data=data,
            headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        bodies = []
        for request in json.loads(response)['requests']:
            bodies.append(request['body'])
        if expected_body in bodies:
            return True
        print(f'Expected "{expected_body}" was not found in actual "{bodies}".')
        return False
