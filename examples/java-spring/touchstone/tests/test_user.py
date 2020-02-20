import json
import urllib.request

from touchstone.lib.mocks import validation
from touchstone.lib.touchstone_test import TouchstoneTest

from tests import creds


class GetUser(TouchstoneTest):
    """
    GIVEN a user
        AND the user exists in the database.
    WHEN a GET request is submitted to the '/user' endpoint with the user's id.
    THEN the user is returned from the endpoint with the correct fields.
    """

    def given(self) -> object:
        given = {
            'id': 999,
            'firstName': 'Jane',
            'lastName': 'Brown',
            'email': 'jane789@example.com'
        }
        self.mocks.mysql.setup.insert_row(creds.MYSQL_DATABASE, creds.MYSQL_TABLE, given)
        return given

    def when(self, given) -> object:
        response = urllib.request.urlopen(f'{self.service_url}/user/{given["id"]}').read()
        return json.loads(response.decode('utf-8'))

    def then(self, given, result) -> bool:
        return validation.matches(given, result)


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
        expected_response = given.copy()
        expected_response['id'] = validation.ANY
        expected_row = given.copy()
        return validation.matches(expected_response, result) and self.mocks.mysql.verify.row_exists(
            creds.MYSQL_DATABASE,
            creds.MYSQL_TABLE,
            expected_row)


class PutUser(TouchstoneTest):
    """
    GIVEN a user's desired new info
        AND the user exists in the database.
    WHEN a PUT request is submitted to the '/user' endpoint with the user's new info.
    THEN the user's info is updated in the database.
    """

    def given(self) -> object:
        new_info = {
            'id': 999,
            'firstName': 'Janie',
            'lastName': 'White',
            'email': 'jane123@example.org'
        }
        existing_user = {
            'id': 999,
            'firstName': 'Jane',
            'lastName': 'Brown',
            'email': 'jane789@example.com'
        }
        self.mocks.mysql.setup.insert_row(creds.MYSQL_DATABASE, creds.MYSQL_TABLE, existing_user)
        return new_info

    def when(self, given) -> object:
        body = bytes(json.dumps(given), encoding='utf-8')
        request = urllib.request.Request(f'{self.service_url}/user', data=body, method='PUT',
                                         headers={'Content-type': 'application/json'})
        urllib.request.urlopen(request)
        return None

    def then(self, given, result) -> bool:
        return self.mocks.mysql.verify.row_exists(creds.MYSQL_DATABASE, creds.MYSQL_TABLE, given)


class DeleteUser(TouchstoneTest):
    """
    GIVEN a user's id
        AND the user exists in the database.
    WHEN a DELETE request is submitted to the '/user' endpoint with the user's id.
    THEN a message is published to the 'user.exchange' with a routing key of 'user-deleted' and a payload with the
    user's id
        AND the user no longer exists in the database.
    """

    def processing_period(self) -> float:
        return 0.5

    def given(self) -> object:
        user_id = 999
        user = {
            'id': user_id,
            'firstName': 'Jane',
            'lastName': 'Brown',
            'email': 'jane789@example.com'
        }
        self.mocks.mysql.setup.insert_row(creds.MYSQL_DATABASE, creds.MYSQL_TABLE, user)
        return user_id

    def when(self, given) -> object:
        request = urllib.request.Request(f'{self.service_url}/user/{given}', method='DELETE')
        urllib.request.urlopen(request)
        return None

    def then(self, given, result) -> bool:
        where = {
            'id': given
        }
        return self.mocks.rabbitmq.verify.payload_published('user.exchange', str(given),
                                                            routing_key='user-deleted') and \
               self.mocks.mysql.verify.row_does_not_exist(creds.MYSQL_DATABASE, creds.MYSQL_TABLE, where)
