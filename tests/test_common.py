import unittest
from unittest import TestCase, mock

from touchstone import common


class TestCommon(TestCase):
    @mock.patch('touchstone.common.os')
    def test_sanityCheckPasses_requirementsMet_ReturnsTrue(self, mock_os):
        # Given
        mock_os.getcwd.return_value = 'temp'
        mock_os.path.exists.return_value = True

        # When
        result = common.sanity_check_passes()

        # Then
        self.assertTrue(result)

    @mock.patch('touchstone.common.os')
    def test_sanityCheckPasses_requirementsNotMet_ReturnsFalse(self, mock_os):
        # Given
        mock_os.getcwd.return_value = 'temp'
        mock_os.path.exists.return_value = False

        # When
        result = common.sanity_check_passes()

        # Then
        self.assertFalse(result)

    def test_dictMerge_emptyOverride_ReturnsBase(self):
        # Given
        base = {'foo': 'bar'}
        override = {}

        # When
        result = common.dict_merge(base, override)

        # Then
        self.assertDictEqual(result, base)

    def test_dictMerge_noOverlap_ReturnsCombined(self):
        # Given
        base = {'foo': 'bar'}
        override = {'bar': 'foo'}

        # When
        result = common.dict_merge(base, override)

        # Then
        expected = {'foo': 'bar', 'bar': 'foo'}
        self.assertDictEqual(result, expected)

    def test_dictMerge_withOverlap_OverrideTakesPrecedence(self):
        # Given
        base = {'foo': 'bar', 'bar': 'foo'}
        override = {'bar': 'buzz'}

        # When
        result = common.dict_merge(base, override)

        # Then
        expoected = {'foo': 'bar', 'bar': 'buzz'}
        self.assertDictEqual(result, expoected)

    def test_toSnake_string_ReturnsSnake(self):
        # Given
        input = 'fooBar'

        # When
        result = common.to_snake(input)

        # Then
        self.assertEqual(result, 'foo_bar')

    def test_toSnake_dict_ReturnsSnakeKeys(self):
        # Given
        input = {'fooKey': 'barValue'}

        # When
        result = common.to_snake(input)

        # Then
        self.assertDictEqual(result, {'foo_key': 'barValue'})

    def test_toSnake_listOfDicts_ReturnsSnakeKeys(self):
        # Given
        input = [{'fooKey': 'barValue'}, {'barKey': 'fooValue'}]

        # When
        result = common.to_snake(input)

        # Then
        self.assertListEqual(result, [{'foo_key': 'barValue'}, {'bar_key': 'fooValue'}])


if __name__ == '__main__':
    unittest.main()
