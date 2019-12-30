import unittest
from unittest import TestCase, mock
from unittest.mock import Mock

from touchstone import common


class TestCommon(TestCase):
    @mock.patch('touchstone.common.sys')
    def test_exitTouchstone_isSuccessful_ExitCode0(self, mock_sys: Mock):
        # Given
        is_successful = True

        # When
        common.exit_touchstone(is_successful)

        # Then
        mock_sys.exit.assert_called_once_with(0)

    @mock.patch('touchstone.common.sys')
    def test_exitTouchstone_isUnSuccessful_ExitCode1(self, mock_sys: Mock):
        # Given
        is_successful = False

        # When
        common.exit_touchstone(is_successful)

        # Then
        mock_sys.exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
