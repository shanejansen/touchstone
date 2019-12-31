import unittest
from unittest import TestCase, mock
from unittest.mock import Mock

from touchstone.lib.mocks.mocks import Mocks
from touchstone.lib.services import Services


class TestServices(TestCase):
    def setUp(self) -> None:
        self.mock_mocks = mock.create_autospec(Mocks)
        self.services = Services(self.mock_mocks)

    def test_start_servicesNotRunning_servicesAreRunning(self):
        # When
        self.services.start()

        # Then
        self.assertTrue(self.services.are_running())

    def test_start_servicesRunning_servicesAreNotRunning(self):
        # Given
        self.services.start()

        # When
        self.services.stop()

        # Then
        self.assertFalse(self.services.are_running())

    @mock.patch('touchstone.lib.services.Service')
    @mock.patch('touchstone.lib.services.TouchstoneConfig')
    def test_runTests_allTestsPass_ReturnsTrue(self, mock_touchstone_config: Mock, mock_service: Mock):
        # Given
        mock_some_service = Mock()
        mock_some_service.run_tests.return_value = True
        mock_service.return_value = mock_some_service
        mock_touchstone_config.instance().config = {'host': 'some-host',
                                                    'root': 'some-path',
                                                    'services': [{'tests': 'some-path'}]}
        self.services = Services(self.mock_mocks)

        # When
        result = self.services.run_tests()

        # Then
        self.assertTrue(result)

    @mock.patch('touchstone.lib.services.Service')
    @mock.patch('touchstone.lib.services.TouchstoneConfig')
    def test_runTests_testFails_ReturnsFalse(self, mock_touchstone_config: Mock, mock_service: Mock):
        # Given
        mock_some_service = Mock()
        mock_some_service.run_tests.return_value = False
        mock_service.return_value = mock_some_service
        mock_touchstone_config.instance().config = {'host': 'some-host',
                                                    'root': 'some-path',
                                                    'services': [{'tests': 'some-path'}]}
        self.services = Services(self.mock_mocks)

        # When
        result = self.services.run_tests()

        # Then
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
