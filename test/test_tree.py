from __future__ import absolute_import

import random
from unittest import TestCase

from logic.generator import PatternGenerator
from models.tree import PatternTree
from logic.values import ValueGenerator


class TestTree(TestCase):

    def test_generation(self):
        fields = ValueGenerator.generate_field_names(10)
        iterations = 100
        pattern_lengths = [random.randint(2, 10) for _ in range(iterations)]
        patterns = []
        for i in range(len(pattern_lengths)):
            patterns.append(PatternGenerator.generate_pattern(pattern_lengths[i], [f for f in fields]))
        # once patterns are generated, check that they are consistent
        for i in range(len(patterns)):
            pattern: PatternTree = patterns[i]
            records = pattern.get_nodes_list()
            # check length
            self.assertEqual(len(records), pattern_lengths[i] + 1)
            # check length of each record
            for record in records:
                self.assertTrue(len(record.fields) <= 10)
