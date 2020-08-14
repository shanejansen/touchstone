import json
import urllib
import urllib.error
import urllib.parse
import urllib.request

from touchstone.lib import exceptions
from touchstone.lib.mocks.networked_runnables.http.i_http_behavior import IHttpSetup


class DockerHttpSetup(IHttpSetup):
    def __init__(self):
        super().__init__()
        self.__url = None
        self.mock_ids: list = []

    def set_url(self, url: str):
        self.__url = url

    def init(self, defaults: dict):
        # Remove all mocked endpoints
        for mock_id in self.mock_ids:
            request = urllib.request.Request(f'{self.__url}/__admin/mappings/{mock_id}', method='DELETE')
            try:
                urllib.request.urlopen(request)
            except urllib.error.HTTPError:
                pass
        self.mock_ids = []

        # Reset requests journal
        request = urllib.request.Request(f'{self.__url}/__admin/requests', method='DELETE')
        urllib.request.urlopen(request)

        for request in defaults.get('requests', []):
            self.__submit_mock(request)

    def get(self, endpoint: str, response: str, response_status: int = 200,
            response_headers: dict = {'Content-Type': 'application/json'}):
        self.__check_mock_response_type(response)
        mock = {
            'request': {
                'method': 'GET',
                'urlPattern': endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_mock(mock)

    def post(self, endpoint: str, response: str, response_status: int = 200,
             response_headers: dict = {'Content-Type': 'application/json'}):
        self.__check_mock_response_type(response)
        mock = {
            'request': {
                'method': 'POST',
                'urlPattern': endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_mock(mock)

    def put(self, endpoint: str, response: str, response_status: int = 200,
            response_headers: dict = {'Content-Type': 'application/json'}):
        self.__check_mock_response_type(response)
        mock = {
            'request': {
                'method': 'PUT',
                'urlPattern': endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_mock(mock)

    def delete(self, endpoint: str, response: str, response_status: int = 200,
               response_headers: dict = {'Content-Type': 'application/json'}):
        self.__check_mock_response_type(response)
        mock = {
            'request': {
                'method': 'DELETE',
                'urlPattern': endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_mock(mock)

    def __check_mock_response_type(self, response):
        if type(response) is not str:
            raise exceptions.MockException('Response must be of type str.')

    def __submit_mock(self, mock: dict):
        data = json.dumps(mock).encode('utf-8')
        request = urllib.request.Request(
            f'{self.__url}/__admin/mappings', data=data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        self.mock_ids.append(json.loads(response)['id'])
