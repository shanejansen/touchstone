import unittest
from unittest import TestCase
from unittest.mock import Mock

from touchstone.lib.service import Service


class TestService(TestCase):
    def setUp(self) -> None:
        self.mock_tests = Mock()
        self.mock_docker_manager = Mock()

    def test_start_dockerfileNotSet_serviceNotStarted(self):
        # Given
        service = Service('', '', self.mock_tests, None, '', 0, '', 0, 0, self.mock_docker_manager)

        # When
        service.start([])

        # Then
        self.mock_docker_manager.run_image.assert_not_called()

    def test_stop_serviceIsRunning_serviceStops(self):
        service = Service('', '', self.mock_tests, '', '', 0, '', 0, 0, self.mock_docker_manager)

        # When
        service.start([])
        service.stop()

        # Then
        self.mock_docker_manager.stop_container.assert_called_once()
        self.assertFalse(service.is_running())


if __name__ == '__main__':
    unittest.main()
