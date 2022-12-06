import unittest
from unittest import TestCase
from unittest.mock import Mock

from touchstone.lib.nodes.deps.deps import Deps


class TestMocks(TestCase):
    def setUp(self) -> None:
        self.mock_http = Mock()
        self.mock_rabbitmq = Mock()
        self.mock_mongodb = Mock()

        self.deps = Deps()

    def test_start_depsNotRunning_depsAreRunning(self):
        # When
        self.deps.start()

        # Then
        self.assertTrue(self.deps.are_running())

    def test_start_depsRunning_depsAreNotRunning(self):
        # Given
        self.deps.start()

        # When
        self.deps.stop()

        # Then
        self.assertFalse(self.deps.are_running())


if __name__ == '__main__':
    unittest.main()
