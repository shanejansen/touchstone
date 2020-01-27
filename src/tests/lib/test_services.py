import unittest
from unittest import TestCase
from unittest.mock import Mock

from touchstone.lib.services import Services


class TestServices(TestCase):
    def test_start_servicesNotRunning_servicesAreRunning(self):
        # Given
        services = Services([])

        # When
        services.start([])

        # Then
        self.assertTrue(services.are_running())

    def test_stop_servicesRunning_servicesAreNotRunning(self):
        # Given
        services = Services([])

        # When
        services.start([])
        services.stop()

        # Then
        self.assertFalse(services.are_running())

    def test_runTests_allTestsPass_ReturnsTrue(self):
        # Given
        mock_service = Mock()
        mock_service.run_all_tests.return_value = True
        services = Services([mock_service])

        # When
        result = services.run_all_tests()

        # Then
        self.assertTrue(result)

    def test_runTests_testFails_ReturnsFalse(self):
        # Given
        mock_service = Mock()
        mock_service.run_all_tests.return_value = False
        services = Services([mock_service])

        # When
        result = services.run_all_tests()

        # Then
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
