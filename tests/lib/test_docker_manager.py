import unittest
from unittest import TestCase, mock
from unittest.mock import Mock

from touchstone.lib import exceptions
from touchstone.lib.managers.docker_manager import DockerManager


class TestDockerManager(TestCase):
    def setUp(self) -> None:
        self.docker_manager = DockerManager(should_auto_discover=False)

    @mock.patch('touchstone.lib.managers.docker_manager.subprocess')
    def test_buildDockerfile_CommandReturnsNon0_exceptionRaised(self, mock_subprocess: Mock):
        # Given
        dockerfile_path = '../'
        mock_subprocess.run.return_value = Mock(**{'returncode': 1})

        # Then
        self.assertRaises(exceptions.ContainerException, self.docker_manager.build_dockerfile, dockerfile_path)

    @mock.patch('touchstone.lib.managers.docker_manager.subprocess')
    def test_runImage_commandReturnsNon0_exceptionRaised(self, mock_subprocess: Mock):
        # Given
        image = 'some-image'
        mock_subprocess.run.return_value = Mock(**{'returncode': 1})

        # Then
        self.assertRaises(exceptions.ContainerException, self.docker_manager.run_background_image, image)
        self.assertFalse(self.docker_manager.containers_running())

    @mock.patch('touchstone.lib.managers.docker_manager.subprocess')
    def test_cleanup_containersRunning_containersNoLongerRunning(self, mock_subprocess: Mock):
        # Given
        mock_subprocess.run.return_value = Mock(**{'returncode': 0, 'stdout': bytes()})

        # When
        self.docker_manager.run_background_image('some-container')
        self.docker_manager.run_background_image('some-container1')
        self.docker_manager.cleanup()

        # Then
        self.assertFalse(self.docker_manager.containers_running())


if __name__ == '__main__':
    unittest.main()
