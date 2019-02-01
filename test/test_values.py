from __future__ import absolute_import

from unittest import TestCase

from logic.values import ValueGenerator


class TestValueGenerator(TestCase):
    def test_random_string(self):
        s = ValueGenerator.random_string()
        self.assertIsInstance(s, str)

    def test_generate_values(self):
        fields = 10
        values = ValueGenerator.generate_field_names(fields)
        self.assertEqual(len(values), fields)
