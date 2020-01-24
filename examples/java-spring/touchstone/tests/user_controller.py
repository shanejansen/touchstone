import json
import urllib.request

from touchstone.lib.mocks import validation
from touchstone.lib.touchstone_test import TouchstoneTest

mysql_database = 'myapp'
mysql_table = 'users'


class GetUser(TouchstoneTest):
    """
    GIVEN a user
        AND the user exists in the database.
    WHEN a GET request is submitted to the '/user' endpoint with the user's id.
    THEN the user is returned from the endpoint with the correct fields.
    """

    def given(self) -> object:
        given = {
            'id': 99,
            'firstName': 'Jane',
            'lastName': 'Brown',
            'email': 'jane789@example.com'
        }
        self.mocks.mysql.setup.insert_row(mysql_database, mysql_table, given)
        return given

    def when(self, given) -> object:
        response = urllib.request.urlopen(f'{self.service_url}/user/{given["id"]}').read()
        return json.loads(response.decode('utf-8'))

    def then(self, given, result) -> bool:
        return validation.expected_matches_actual(given, result)


class PostUser(TouchstoneTest):
    """
    GIVEN a user's first name, last name, and email
        AND the email API returns the user's email.
    WHEN a POST request is submitted to the '/user' endpoint with the user's first name and last name.
    THEN the user is returned from the endpoint with the correct fields
        AND the user is saved to the database.
    """

    def given(self) -> object:
        given = {
            'firstName': 'Jane',
            'lastName': 'Brown',
            'email': 'jane789@example.com'
        }
        self.mocks.http.setup.get('/jane-brown/email', given['email'])
        return given

    def when(self, given) -> object:
        body = {
            'firstName': given['firstName'],
            'lastName': given['lastName']
        }
        body = bytes(json.dumps(body), encoding='utf-8')
        request = urllib.request.Request(f'{self.service_url}/user', data=body,
                                         headers={'Content-type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        return json.loads(response.decode('utf-8'))

    def then(self, given, result) -> bool:
        expected = given
        self.mocks.mysql.verify.row_exists(mysql_database, mysql_table, expected)
        return validation.expected_matches_actual(expected, result)


class DeleteUser(TouchstoneTest):
    """
    GIVEN a user's id.
    WHEN a DELETE request is submitted to the '/user' endpoint with the user's id.
    THEN a message is published to the 'user.exchange' with a routing key of 'user-deleted' and a payload with the
    user's id.
    """

    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        return {
            'userId': 1
        }

    def when(self, given) -> object:
        request = urllib.request.Request(f'{self.service_url}/user/{given["userId"]}', method='DELETE')
        urllib.request.urlopen(request)
        return None

    def then(self, given, result) -> bool:
        return self.mocks.rabbitmq.verify.payload_published('user.exchange', str(given['userId']),
                                                            routing_key='user-deleted')
