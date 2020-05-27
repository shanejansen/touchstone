import unittest
from unittest import TestCase

from touchstone import common


class TestCommon(TestCase):
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
