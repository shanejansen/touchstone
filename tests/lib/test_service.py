import unittest
from unittest import TestCase
from unittest.mock import Mock

from touchstone.lib.services.networked_service import NetworkedService


class TestService(TestCase):
    def setUp(self) -> None:
        self.mock_tests = Mock()
        self.mock_docker_manager = Mock()

    def test_start_dockerfileNotSet_serviceNotStarted(self):
        # Given
        service = NetworkedService('', self.mock_tests, None, self.mock_docker_manager, '', '', '', 0, 0)

        # When
        service.start([])

        # Then
        self.mock_docker_manager.run_image.assert_not_called()

    def test_stop_serviceIsRunning_serviceStops(self):
        service = NetworkedService('', self.mock_tests, '', self.mock_docker_manager, '', '', '', 0, 0)

        # When
        service.start([])
        service.stop()

        # Then
        self.mock_docker_manager.stop_container.assert_called_once()
        self.assertFalse(service.is_running())


if __name__ == '__main__':
    unittest.main()
