import unittest
import urllib.error
from unittest import TestCase, mock
from unittest.mock import Mock

from touchstone.lib.configs.service_config import ServiceConfig
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.service import Service
from touchstone.lib.tests import Tests


class TestService(TestCase):
    def setUp(self) -> None:
        self.mock_service_config = mock.create_autospec(ServiceConfig)
        self.mock_tests = mock.create_autospec(Tests)
        self.service = Service(self.mock_service_config, self.mock_tests)

    @mock.patch('touchstone.lib.service.DockerManager')
    def test_start_dockerfileNotSet_serviceNotStarted(self, mock_docker_manager: Mock):
        # Given
        self.mock_service_config.config = {'dockerfile': None}
        self.service = Service(self.mock_service_config, self.mock_tests)

        # When
        self.service.start()

        # Then
        mock_docker_manager.instance().run_image.assert_not_called()

    @mock.patch('touchstone.lib.service.TouchstoneConfig')
    @mock.patch('touchstone.lib.service.DockerManager')
    def test_stop_serviceIsRunning_serviceStops(self, mock_docker_manager: Mock,
                                                mock_touchstone_config: TouchstoneConfig):
        # Given
        mock_docker_manager.instance().run_image.return_value = 'some-image-tag'
        mock_touchstone_config.instance().config = {'root': 'some-root'}
        self.mock_service_config.config = {'name': 'some-service',
                                           'dockerfile': 'some-dockerfile',
                                           'port': 'some-port'}
        self.service = Service(self.mock_service_config, self.mock_tests)

        # When
        self.service.start()
        self.service.stop()

        # Then
        mock_docker_manager.instance().stop_container.assert_called_once()
        self.assertFalse(self.service.is_running())

    @mock.patch('touchstone.lib.service.urllib.request')
    def test_runTests_ServiceUnavailable_ReturnsFalse(self, mock_request: Mock):
        # Given
        mock_request.urlopen.side_effect = urllib.error.URLError('some-reason')
        self.mock_service_config.config = {'name': 'some-service',
                                           'url': 'some-url',
                                           'availability_endpoint': 'some-endpoint',
                                           'num_retries': 1,
                                           'seconds_between_retries': 0}
        self.service = Service(self.mock_service_config, self.mock_tests)

        # When
        result = self.service.run_tests()

        # Then
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
