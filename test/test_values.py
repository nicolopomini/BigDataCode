from __future__ import absolute_import

from unittest import TestCase

from src.values import ValueGenerator


class TestValueGenerator(TestCase):
    def test_random_string(self):
        s = ValueGenerator.random_string()
        self.assertIsInstance(s, str)

    def test_generate_values(self):
        fields = 10
        vals = 10
        values = ValueGenerator.generate_values(fields, vals)
        self.assertEqual(len(values), fields)
        for f in values:
            self.assertEqual(len(values[f]), vals)
