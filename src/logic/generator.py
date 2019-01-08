from __future__ import absolute_import

from typing import List, Dict

from models.tree import TreePattern, TransactionTree
from logic.values import ValueGenerator
import random
import copy
import numpy as np


class PatternGenerator:
    @staticmethod
    def generate_pattern(length: int, fields: List[str], values: Dict[str, List[str]], max_fields_for_record: int) -> TreePattern:
        """
        Create a pattern, which is a tree
        :param length: length of the pattern, at least 1. It is the number of edges. Number of nodes: 1 + length
        :param fields: list of the field names
        :param values: list of values: {field_name => list of possible values}
        :param max_fields_for_record: max number of field each record has (excluded the 3 mandatory)
        :return: the TreePattern, route of the pattern
        """
        if length < 1:
            raise ValueError("The length must be at least 1. Given %d" % length)
        if max_fields_for_record < 1:
            raise ValueError("Each record must have at least one field")
        # first, create all nodes
        nodes = []
        while len(nodes) < length + 1:
            # record in the pattern with multiple fields
            number_of_fields = random.randint(1, max_fields_for_record)
            fields_for_record: Dict[str, str] = {}
            for _ in range(number_of_fields):
                field_name = fields[random.randint(0, len(fields) - 1)]
                field_value = values[field_name][random.randint(0, len(values[field_name]) - 1)]
                fields_for_record[field_name] = field_value
            node = TreePattern(fields_for_record)
            if node not in nodes:  # quick fix to force nodes to be different either in field or value
                nodes.append(node)
        # second, build the tree, choosing randomly where to append
        # another random choice is to create an empty node, which represents any value
        root: TreePattern = nodes[random.randint(0, len(nodes) - 1)]
        included = [root]
        nodes.remove(root)
        for _ in range(length):
            parent = included[random.randint(0, len(included) - 1)]
            # with prob = 20%, create an empty node
            if random.randint(1, 5) == 1:
                child = TreePattern({})
            else:
                child = nodes[random.randint(0, len(nodes) - 1)]
                nodes.remove(child)
            parent.add_child(child)
            included.append(child)
        return root


class TransactionGenerator:
    MIN_FREQ_PERC = 0.2
    TRANSACTION_PATTERN_PERC = 0.3

    def __init__(self, total_trees: int, total_patterns: int, avg_pattern_length: float, fields: int, values_for_field: int, threshold: int, print_pattern: bool = False) -> None:
        """
        Create a node that is part of a pattern
        :param total_trees: the total number of trees that will be generated
        :param total_patterns: the total number of patterns that will be used
        :param avg_pattern_length: the average number of edges a pattern can have
        :param fields: number of fields each record has. It has to be at least 4
        :param values_for_field: number of values each field can assume
        :param threshold: number of times a pattern has to appear to be a pattern
        :param print_pattern: if true, the generated pattern are printed
        """
        if total_trees < 1:
            raise ValueError("There must be at least one tree. Given %d" % total_trees)
        if avg_pattern_length < 1:
            raise ValueError("There must be at least 2 nodes in a pattern. Given %d" % avg_pattern_length)
        if fields < 4:
            raise ValueError("The number of filed must be at least 4, given %d" % fields)
        if values_for_field < 1:
            raise ValueError("Each field must assume a value.")
        if threshold < 1:
            raise ValueError("A pattern must appear at least once. Given %d" % threshold)
        self.total_patterns: int = total_patterns
        self.total_trees: int = total_trees
        self.avg_pattern_length = avg_pattern_length
        self.fields = fields
        self.values_for_field = values_for_field
        self.threshold = threshold
        self.print_pattern = print_pattern

    def tree_pattern_to_transaction_tree(self, original: TreePattern, data: Dict[str, List[str]], parent: TransactionTree = None) -> TransactionTree:
        rid = ValueGenerator.random_string()
        attributes = {"rid": rid, "parent": "" if parent is None else parent.fields["rid"]}
        # add attributes of the pattern
        for field in original.fields:
            attributes[field] = original.fields[field]
        for field in data:
            if field not in attributes:
                attributes[field] = data[field][random.randint(0, len(data[field]) - 1)]
        node = TransactionTree(attributes)
        for tree in original.children:
            node.add_child(self.tree_pattern_to_transaction_tree(tree, data, node))
        return node


    @staticmethod
    def _print_patterns(patterns: List[TreePattern], appearances: List[List[int]]) -> None:
        print("GENERATION DETAILS:\n")
        print("Generated patterns: %d\n" % len(patterns))
        for i in range(len(patterns)):
            patterns[i].print_tree()
            print("Appeares %d times" % len(appearances[i]))

    def generate_data(self) -> List[Dict[str, str]]:
        # Patterns are generated
        pattern_list: List[TreePattern] = []
        attributes = ValueGenerator.generate_pattern_values(self.fields, self.values_for_field)     # global list of attributes
        fields = [field for field in attributes]
        len_min = 1000
        len_max = 0
        for _ in range(self.total_patterns):
            pattern_length = int(max(1, np.random.poisson(self.avg_pattern_length)))
            if pattern_length < len_min:
                len_min = pattern_length
            if pattern_length > len_max:
                len_max = pattern_length
            pattern_list.append(PatternGenerator.generate_pattern(pattern_length, fields, attributes, self.fields - 3))
        pattern_transactions = []   # pattern i => list of transactions it will appear on
        for _ in range(len(pattern_list)):
            p_transactions = []
            number_of_appearences: int = 10     #TODO: change this value (create a function depending on length)
            for _ in range(number_of_appearences):
                p_transactions.append(random.randint(0, self.total_trees - 1))
            pattern_transactions.append(p_transactions)
        # if print flag is set, print details
        if self.print_pattern:
            TransactionGenerator._print_patterns(pattern_list, pattern_transactions)

        # change TreePattern nodes into TransactionTree nodes
        pattern_for_transaction = []

        # TODO: change TreePattern nodes into TransactionTree nodes using tree_pattern_to_transaction_tree
        # TODO: test
        # TODO: read arguments in the main script and use them
        # TODO: update README with instructions

        return None
        """
        pattern_tree_indexes = {}
        for pattern in pattern_list:
            tree_indexes = []
            min_frequency = int(self.total_trees * TransactionGenerator.MIN_FREQ_PERC)
            for _ in range(self.total_trees - (((len(pattern.get_nodes_list()) - 1) - self.min_pattern_nodes) * ((self.total_trees - min_frequency) / (self.max_pattern_nodes - self.min_pattern_nodes)))):
                tree_indexes.append(random.randint(0, self.total_trees - 1))
            pattern_tree_indexes[pattern] = tree_indexes
            print("indexes: " + str(len(tree_indexes)) + " pattern: " + str(len(pattern.get_nodes_list())-1))
        # Trees are generated
        tree_list: List[TreePattern] = []
        for index in range(self.total_trees):
            chosen_patterns = []
            for pattern in pattern_list:
                if index in pattern_tree_indexes[pattern]:
                    chosen_patterns.append(pattern)
            attributes = ValueGenerator.generate_values(fields, vals)   # new fields and values for the randomly generated nodes
            fields_list = list(attributes.keys())
            random_nodes = []
            # Random nodes generation
            while len(random_nodes) < (self.max_pattern_nodes + self.min_pattern_nodes) + (self.max_pattern_nodes + self.min_pattern_nodes) * len(chosen_patterns):
                field_name = fields_list[random.randint(0, len(fields_list) - 1)]
                field_value = attributes[field_name][random.randint(0, len(attributes[field_name]) - 1)]
                node = TreePattern(field_name, field_value)
                if node not in random_nodes:  # quick fix to force nodes to be different either in field or value
                    random_nodes.append(node)
            # Randomly append orphan nodes and patterns
            random_nodes.extend(chosen_patterns)
            selected_root = random_nodes[random.randint(0, len(random_nodes) - 1)]
            root = copy.deepcopy(selected_root)
            current_tree = []
            if selected_root in chosen_patterns:
                current_tree.extend(root.get_nodes_list())
            else:
                current_tree.append(root)
            random_nodes.remove(selected_root)
            while len(random_nodes) > 0:
                selected_node_to_append = random_nodes[random.randint(0, len(random_nodes) - 1)]
                node_to_append = copy.deepcopy(selected_node_to_append)
                chosen_parent = current_tree[random.randint(0, len(current_tree) - 1)]
                if "_____" not in chosen_parent.field:
                    chosen_parent.add_child(node_to_append)
                    if selected_node_to_append in chosen_patterns:
                        current_tree.extend(node_to_append.get_nodes_list())
                    else:
                        current_tree.append(node_to_append)
                    random_nodes.remove(selected_node_to_append)
                else:
                    if selected_node_to_append not in chosen_patterns:
                        chosen_parent.add_child(node_to_append)
                        current_tree.append(node_to_append)
                        random_nodes.remove(selected_node_to_append)
            tree_list.append(root)
        return tree_list
        """
