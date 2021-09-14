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

    def test_matches_MatchingANYWithList_ReturnsTrue(self):
        # Given
        expected = {'foo': [{'bar': validation.ANY}]}
        actual = {'foo': [{'bar': 'buzz'}]}

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_MatchingANYWithNestedList_ReturnsTrue(self):
        # Given
        expected = [{'bar': [{'bazz': validation.ANY}]}]
        actual = [{'bar': [{'bazz': 'buzz'}]}]

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_MatchingListOfStrings_ReturnsTrue(self):
        # Given
        expected = ['foo']
        actual = ['foo']

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_MatchingListOfDicts_ReturnsTrue(self):
        # Given
        expected = [{'foo': 'bar'}]
        actual = [{'foo': 'bar'}]

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_MatchingListOfLists_ReturnsTrue(self):
        # Given
        expected = [['foo']]
        actual = [['foo']]

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_MatchingListOfStringsOutOfOrder_ReturnsTrue(self):
        # Given
        expected = ['foo', 'bar']
        actual = ['bar', 'foo']

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_MatchingListOfDictsOutOfOrder_ReturnsTrue(self):
        # Given
        expected = [{'foo': 'bar'}, {'bazz': 'buzz'}]
        actual = [{'bazz': 'buzz'}, {'foo': 'bar'}]

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_MatchingListOfListsOutOfOrder_ReturnsTrue(self):
        # Given
        expected = [['foo'], ['bar']]
        actual = [['bar'], ['foo']]

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_MatchingListWithANY_ReturnsTrue(self):
        # Given
        expected = ['foo', validation.ANY, 'bar']
        actual = ['foo', 'bazz', 'bar']

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertTrue(result)

    def test_matches_NonMatchingListWithANY_ReturnsFalse(self):
        # Given
        expected = ['foo', validation.ANY, 'bar']
        actual = ['foo', 'bazz', 'buzz']

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertFalse(result)

    def test_matches_MatchingListWithMultipleANY_ReturnsTrue(self):
        # Given
        expected = ['foo', validation.ANY, validation.ANY]
        actual = ['foo', 'bazz', 'bar']

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

    def test_matches_NonMatchingDictValueTypesExpectListActualDict_ReturnsFalse(self):
        # Given
        expected = {
            'foo': ['bar']
        }
        actual = {
            'foo': {'bar': 'bar'}
        }

        # When
        result = validation.matches(expected, actual)

        # Then
        self.assertFalse(result)

    def test_matches_NonMatchingDictValueTypesExpectDictActualList_ReturnsFalse(self):
        # Given
        expected = {
            'foo': {'bar': 'bar'}
        }
        actual = {
            'foo': ['bar']
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
