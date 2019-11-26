import json
import urllib.request

from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.mocks.mock_case import Verify


class HttpVerify(Verify):
    def __init__(self, exposed_port: int):
        super().__init__(exposed_port)

    def get_called(self, endpoint: str, times: int = None) -> bool:
        return self.__count_verification(endpoint, 'GET', times)

    def post_called(self, endpoint: str, times: int = None) -> bool:
        return self.__count_verification(endpoint, 'POST', times)

    def put_called(self, endpoint: str, times: int = None) -> bool:
        return self.__count_verification(endpoint, 'PUT', times)

    def delete_called(self, endpoint: str, times: int = None) -> bool:
        return self.__count_verification(endpoint, 'DELETE', times)

    def post_contained(self, expected_payload: str, call_num: int = 1) -> bool:
        return False

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
        return times == call_count
