import unittest
from unittest import TestCase

from touchstone.lib.mocks.mocks import Mocks


class TestMocks(TestCase):
    def setUp(self) -> None:
        self.mocks = Mocks()

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
