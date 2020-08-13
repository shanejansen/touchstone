import unittest
from unittest import TestCase

from touchstone.helpers import validation


class TestValidation(TestCase):
    def test_matches_MatchingStrings_ReturnsTrue(self):
        # Given
        expected = 'foo'
        actual = 'foo'

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_MatchingANY_ReturnsTrue(self):
        # Given
        expected = validation.ANY
        actual = 'foo'

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_NonMatchingStrings_ReturnsFalse(self):
        # Given
        expected = 'foo'
        actual = 'bar'

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertFalse(result)

    def test_matches_MatchingDict_ReturnsTrue(self):
        # Given
        expected = {
            'foo': 'bar'
        }
        actual = {
            'foo': 'bar'
        }

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_NonMatchingDict_ReturnsFalse(self):
        # Given
        expected = {
            'foo': 'bar'
        }
        actual = {
            'foo': 'foo'
        }

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertFalse(result)

    def test_matches_MatchingNestedDict_ReturnsTrue(self):
        # Given
        expected = {
            'foo': {
                'nested': 'buzz'
            },
            'bar': {
                'buzz': 'baz'
            }
        }
        actual = {
            'foo': {
                'nested': 'buzz'
            },
            'bar': {
                'buzz': 'baz'
            }
        }

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_ExpectedHasExtraNestedField_ReturnsFalse(self):
        # Given
        expected = {
            'foo': 'foo',
            'bar': {
                'buzz': 'baz'
            }
        }
        actual = {
            'foo': 'foo',
            'bar': {
            }
        }

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertFalse(result)

    def test_matches_ActualHasExtraNestedField_ReturnsFalse(self):
        # Given
        expected = {
            'foo': 'foo',
            'bar': {
            }
        }
        actual = {
            'foo': 'foo',
            'bar': {
                'buzz': 'baz'
            }
        }

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertFalse(result)

    def test_matches_ExpectedHasNestedANY_ReturnsTrue(self):
        # Given
        expected = {
            'foo': 'foo',
            'bar': {
                'buzz': validation.ANY
            }
        }
        actual = {
            'foo': 'foo',
            'bar': {
                'buzz': 'baz'
            }
        }

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
