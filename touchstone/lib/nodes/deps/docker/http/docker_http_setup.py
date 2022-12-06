import json
import urllib
import urllib.error
import urllib.parse
import urllib.request

from touchstone.lib import exceptions
from touchstone.lib.nodes.deps.behaviors.i_http_behavior import IHttpSetup


class DockerHttpSetup(IHttpSetup):
    def __init__(self):
        super().__init__()
        self.__url = None
        self.dep_ids: list = []

    def set_url(self, url: str):
        self.__url = url

    def init(self, defaults: dict):
        # Remove all endpoints
        for dep_id in self.dep_ids:
            request = urllib.request.Request(f'{self.__url}/__admin/mappings/{dep_id}', method='DELETE')
            try:
                urllib.request.urlopen(request)
            except urllib.error.HTTPError:
                pass
        self.dep_ids = []

        # Reset requests journal
        request = urllib.request.Request(f'{self.__url}/__admin/requests', method='DELETE')
        urllib.request.urlopen(request)

        for request in defaults.get('requests', []):
            self.__submit_dep(request)

    def get(self, endpoint: str, response: str, response_status: int = 200, url_pattern: bool = False,
            response_headers: dict = {'Content-Type': 'application/json'}):
        self.__check_dep_response_type(response)
        dep = {
            'request': {
                'method': 'GET',
                self.__get_url_type(url_pattern): endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_dep(dep)

    def post(self, endpoint: str, response: str, response_status: int = 200, url_pattern: bool = False,
             response_headers: dict = {'Content-Type': 'application/json'}):
        self.__check_dep_response_type(response)
        dep = {
            'request': {
                'method': 'POST',
                self.__get_url_type(url_pattern): endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_dep(dep)

    def put(self, endpoint: str, response: str, response_status: int = 200, url_pattern: bool = False,
            response_headers: dict = {'Content-Type': 'application/json'}):
        self.__check_dep_response_type(response)
        dep = {
            'request': {
                'method': 'PUT',
                self.__get_url_type(url_pattern): endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_dep(dep)

    def delete(self, endpoint: str, response: str, response_status: int = 200, url_pattern: bool = False,
               response_headers: dict = {'Content-Type': 'application/json'}):
        self.__check_dep_response_type(response)
        dep = {
            'request': {
                'method': 'DELETE',
                self.__get_url_type(url_pattern): endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_dep(dep)

    def __get_url_type(self, url_pattern: bool):
        if url_pattern:
            return 'urlPattern'
        return 'url'

    def __check_dep_response_type(self, response):
        if type(response) is not str:
            raise exceptions.DepException('Response must be of type str.')

    def __submit_dep(self, dep: dict):
        data = json.dumps(dep).encode('utf-8')
        request = urllib.request.Request(
            f'{self.__url}/__admin/mappings', data=data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        self.dep_ids.append(json.loads(response)['id'])
