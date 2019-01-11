from __future__ import absolute_import

import random
from unittest import TestCase

from logic.generator import TransactionGenerator, PatternGenerator
from models import tree
from logic.values import ValueGenerator


class TestGenerator(TestCase):
    def test_tree_count(self):
        tree_count = 100
        pattern_count = 20
        g = TransactionGenerator(tree_count, pattern_count, 5, 10, 100, 3)
        tree_list = g.generate_data()
        self.assertEqual(len(tree_list), tree_count)

    def test_translation(self):
        number_of_fields = 10
        generator = TransactionGenerator(15, 15, 4, number_of_fields, 100, 1)
        patterns = []
        for _ in range(10 + random.randint(0, 90)):
            patterns.append(PatternGenerator.generate_pattern(2 + random.randint(0, 5), [f for f in generator.attributes], generator.attributes, number_of_fields))
        nodes = []
        for pattern in patterns:
            nodes.append(generator.tree_pattern_to_transaction_tree(pattern))
        for node in nodes:
            self.assertEqual(len(node.fields), number_of_fields - 1)    # tid excluded
            self.assertTrue("rid" in node.fields)
            self.assertTrue("parent" in node.fields)

    def test_attribute_count(self):
        number_of_fields = 10
        generator = TransactionGenerator(100, 10, 5, number_of_fields, 100, 20)
        roots = generator.generate_data()
        for root in roots:
            for record in root.get_nodes_list():
                self.assertEqual(len(record.fields),number_of_fields)