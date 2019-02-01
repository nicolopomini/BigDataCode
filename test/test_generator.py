from __future__ import absolute_import

import random
from unittest import TestCase

from logic.generator import TransactionGenerator, PatternGenerator


class TestGenerator(TestCase):
    def test_tree_count(self):
        tree_count = 100
        pattern_count = 20
        g = TransactionGenerator(tree_count, pattern_count, 5, 10, 3)
        tree_list = g.generate_data()
        self.assertEqual(len(tree_list), tree_count)

    def test_translation(self):
        number_of_fields = 10
        generator = TransactionGenerator(15, 15, 4, number_of_fields, 1)
        patterns = []
        for _ in range(10 + random.randint(0, 90)):
            patterns.append(PatternGenerator.generate_pattern(2 + random.randint(0, 5), [f for f in generator.attributes]))
        nodes = []
        for pattern in patterns:
            nodes.append(generator.tree_pattern_to_transaction_tree(pattern))
        for node in nodes:
            self.assertLessEqual(len(node.fields), number_of_fields - 1)
            self.assertTrue("rid" in node.fields)
            self.assertTrue("parent" in node.fields)

    def test_attribute_count(self):
        number_of_fields = 10
        generator = TransactionGenerator(100, 10, 5, number_of_fields, 20)
        roots = generator.generate_data()
        for root in roots:
            for record in root.get_nodes_list():
                self.assertEqual(len(record.fields), number_of_fields)

    def test_total(self):
        transactions = 10
        patterns = 4
        avg_pattern_length = 3
        number_of_fields = 10
        threshold = 3
        generator = TransactionGenerator(transactions, patterns, avg_pattern_length, number_of_fields, threshold,)
        trees = generator.generate_data()
        for tree in trees:
            nodes = tree.get_nodes_list()
            for node in nodes:
                self.assertTrue("rid" in node.fields)
                self.assertTrue("tid" in node.fields)
                self.assertTrue("parent" in node.fields)
                print(len(node.fields))
