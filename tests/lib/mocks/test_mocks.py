import unittest
from unittest import TestCase
from unittest.mock import Mock

from touchstone.lib.mocks.mocks import Mocks


class TestMocks(TestCase):
    def setUp(self) -> None:
        self.mock_http = Mock()
        self.mock_rabbitmq = Mock()
        self.mock_mongodb = Mock()

        self.mocks = Mocks()
        self.mocks.http = self.mock_http
        self.mocks.register_mock(self.mock_http)
        self.mocks.rabbitmq = self.mock_rabbitmq
        self.mocks.register_mock(self.mock_rabbitmq)
        self.mocks.mongodb = self.mock_mongodb
        self.mocks.register_mock(self.mock_mongodb)

    def test_start_mocksNotRunning_mocksAreRunning(self):
        # When
        self.mocks.start()

        # Then
        self.assertTrue(self.mocks.are_running())

    def test_start_mocksRunning_mocksAreNotRunning(self):
        # Given
        self.mocks.start()

        # When
        self.mocks.stop()

        # Then
        self.assertFalse(self.mocks.are_running())


if __name__ == '__main__':
    unittest.main()
