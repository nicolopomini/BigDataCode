from __future__ import absolute_import

from unittest import TestCase

from logic.generator import TransactionGenerator


class TestGenerator(TestCase):
    def test_tree_count(self):
        tree_count = 100
        pattern_count = 20
        min_pattern_length = 1
        max_pattern_length = 10
        g = TransactionGenerator(tree_count, pattern_count, min_pattern_length, max_pattern_length)
        treelist = g.generate_data()
        self.assertEqual(tree_count, len(treelist))

    def test_tree_length(self):
        tree_count = 100
        pattern_count = 20
        min_pattern_length = 1
        max_pattern_length = 10
        expected_max_length = ((min_pattern_length + max_pattern_length) + (min_pattern_length + max_pattern_length) * pattern_count) + (pattern_count * max_pattern_length)
        expected_min_length = (min_pattern_length + max_pattern_length)
        g = TransactionGenerator(tree_count, pattern_count, min_pattern_length, max_pattern_length)
        treelist = g.generate_data()
        for root in treelist:
            self.assertTrue(expected_min_length <= len(root.get_nodes_list()) <= expected_max_length)