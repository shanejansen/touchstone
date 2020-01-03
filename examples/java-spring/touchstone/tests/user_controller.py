import json
import urllib.request

from touchstone.lib.mocks import validation
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.touchstone_test import TouchstoneTest


class PostUser(TouchstoneTest):
    def __init__(self, service_url: str, mocks: Mocks):
        super().__init__(service_url, mocks)

    def given(self) -> object:
        given = {
            'first_name': 'Jane',
            'last_name': 'Brown',
            'email': 'jane789@example.com'
        }
        self.mocks.http.setup.get('/jane-brown/email', given['email'])
        return given

    def when(self, given) -> object:
        body = {
            'firstName': given['first_name'],
            'lastName': given['last_name']
        }
        body = bytes(json.dumps(body), encoding='utf-8')
        request = urllib.request.Request(f'{self.service_url}/user', data=body,
                                         headers={'Content-type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        return json.loads(response.decode('utf-8'))

    def then(self, given, result) -> bool:
        expected = {
            'id': 0,
            'firstName': given['first_name'],
            'lastName': given['last_name'],
            'email': given['email']
        }
        return validation.expected_matches_actual(expected, result)


class DeleteUser(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        return {
            'user_id': 1
        }

    def when(self, given) -> object:
        request = urllib.request.Request(f'{self.service_url}/user/{given["user_id"]}', method='DELETE')
        urllib.request.urlopen(request)
        return None

    def then(self, given, result) -> bool:
        return self.mocks.rabbitmq.verify.payload_published('user.exchange', str(given['user_id']),
                                                            routing_key='user-deleted')
