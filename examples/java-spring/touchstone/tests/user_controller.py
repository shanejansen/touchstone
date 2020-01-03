import json
import urllib.request

from touchstone.lib.mocks import validation
from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.touchstone_test import TouchstoneTest


class PostUser(TouchstoneTest):
    def __init__(self, service_url: str, mocks: Mocks):
        super().__init__(service_url, mocks)

    def given(self):
        self.mocks.http.setup.get('/jane-brown/email', 'jane789@example.com')

    def when(self):
        body = {
            'firstName': 'Jane',
            'lastName': 'Brown'
        }
        body = bytes(json.dumps(body), encoding='utf-8')
        request = urllib.request.Request(f'{self.service_url}/user', data=body,
                                         headers={'Content-type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        return json.loads(response.decode('utf-8'))

    def then(self, test_result) -> bool:
        expected = {
            'id': 0,
            'firstName': 'Jane',
            'lastName': 'Brown',
            'email': 'jane789@example.com'
        }
        return validation.expected_matches_actual(expected, test_result)


class DeleteUser(TouchstoneTest):
    def processing_period(self) -> float:
        return 0.5

    def given(self):
        pass

    def when(self):
        request = urllib.request.Request(f'{self.service_url}/user/1', method='DELETE')
        urllib.request.urlopen(request)

    def then(self, test_result) -> bool:
        return self.mocks.rabbitmq.verify.payload_published('user.exchange', '1', routing_key='user-deleted')
