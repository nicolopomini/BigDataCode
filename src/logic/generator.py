from __future__ import absolute_import

from typing import List, Dict

from models.tree import PatternTree, TransactionTree
from logic.values import ValueGenerator
import random
import copy
import numpy as np
import math

class PatternGenerator:
    @staticmethod
    def generate_pattern(length: int, fields: List[str], values: Dict[str, List[str]], max_fields_for_record: int) -> PatternTree:
        """
        Create a pattern, which is a tree
        :param length: length of the pattern, at least 1. It is the number of edges. Number of nodes: 1 + length
        :param fields: list of the field names
        :param values: list of values: {field_name => list of possible values}
        :param max_fields_for_record: max number of field each record has (excluded the 3 mandatory)
        :return: the PatternTree, route of the pattern
        """
        if length < 1:
            raise ValueError("The length must be at least 1. Given %d" % length)
        if max_fields_for_record < 1:
            raise ValueError("Each record must have at least one field")
        # first, create all nodes
        nodes = []
        while len(nodes) < length + 1:
            # record in the pattern with multiple fields
            number_of_fields = random.randint(1, min(max_fields_for_record, len(fields)))
            fields_for_record: Dict[str, str] = {}
            fields_name = [f for f in fields]
            for _ in range(number_of_fields):
                field_name = fields_name[random.randint(0, len(fields_name) - 1)]
                field_value = values[field_name][random.randint(0, len(values[field_name]) - 1)]
                fields_for_record[field_name] = field_value
                fields_name.remove(field_name)
            node = PatternTree(fields_for_record)
            if node not in nodes:  # quick fix to force nodes to be different either in field or value
                nodes.append(node)
        # second, build the tree, choosing randomly where to append
        # another random choice is to create an empty node, which represents any value
        root: PatternTree = nodes[random.randint(0, len(nodes) - 1)]
        included = [root]
        nodes.remove(root)
        for _ in range(length):
            parent = included[random.randint(0, len(included) - 1)]
            # with prob = 20%, create an empty node
            if random.randint(1, 5) == 1:
                child = PatternTree({})
            else:
                child = nodes[random.randint(0, len(nodes) - 1)]
                nodes.remove(child)
            parent.add_child(child)
            included.append(child)
        return root


class TransactionGenerator:

    def __init__(self, total_trees: int, total_patterns: int, avg_pattern_length: float, fields: int, values_per_field: int, threshold: int, print_pattern: bool = False) -> None:
        """
        Create a node that is part of a pattern
        :param total_trees: the total number of trees that will be generated
        :param total_patterns: the total number of patterns that will be used
        :param avg_pattern_length: the average number of edges a pattern can have
        :param fields: number of fields each record has. It has to be at least 4
        :param values_per_field: number of values each field can assume
        :param threshold: number of times a pattern has to appear to be a pattern
        :param print_pattern: if true, the generated pattern are printed
        """
        if total_trees < 1:
            raise ValueError("There must be at least one tree. Given %d" % total_trees)
        if avg_pattern_length < 1:
            raise ValueError("There must be at least 2 nodes in a pattern. Given %d" % avg_pattern_length)
        if fields < 4:
            raise ValueError("The number of filed must be at least 4, given %d" % fields)
        if values_per_field < 1:
            raise ValueError("Each field must assume a value.")
        if threshold < 1:
            raise ValueError("A pattern must appear at least once. Given %d" % threshold)
        self.total_patterns: int = total_patterns
        self.total_trees: int = total_trees
        self.avg_pattern_length = avg_pattern_length
        self.fields = fields
        self.values_for_field = values_per_field
        self.threshold = threshold
        self.print_pattern = print_pattern
        self.attributes = ValueGenerator.generate_values(self.fields - 3, self.values_for_field)    # exclude rid, tid and parent

    def tree_pattern_to_transaction_tree(self, original: PatternTree, parent: TransactionTree = None) -> TransactionTree:
        rid = ValueGenerator.random_string()
        attributes = {"rid": rid}
        # add attributes of the pattern
        for field in original.fields:
            attributes[field] = original.fields[field]
        node = TransactionTree(attributes, rid)
        node.parent = parent
        node.fields["parent"] = None if parent is None else parent.rid
        for tree in original.children:
            node.add_child(self.tree_pattern_to_transaction_tree(tree, node))
        return node

    def populate_transaction_pattern(self, to_populate: TransactionTree, tid: str):
        to_populate.fields["tid"] = tid
        to_populate.rid = ValueGenerator.random_string()
        to_populate.fields["rid"] = to_populate.rid
        for field in self.attributes:
            if field not in to_populate.fields:
                to_populate.fields[field] = self.attributes[field][random.randint(0, len(self.attributes[field]) - 1)]
        for child in to_populate.children:
            child.parent = to_populate.rid
            child.fields["parent"] = to_populate.rid
            self.populate_transaction_pattern(child, tid)

    @staticmethod
    def _print_patterns(patterns: List[PatternTree]) -> None:
        print("GENERATION DETAILS:\n")
        print("Generated patterns: %d\n" % len(patterns))
        for i in range(len(patterns)):
            print("Pattern %d:\n" % (i+1))
            patterns[i].print_tree()
            print("\n")

    def generate_data(self) -> List[TransactionTree]:
        # Patterns are generated
        pattern_list: List[PatternTree] = []
        fields = [field for field in self.attributes]
        pattern_min_length = math.inf
        pattern_max_length = 0
        for _ in range(self.total_patterns):
            pattern_length = int(max(1, np.random.poisson(self.avg_pattern_length)))
            if pattern_length < pattern_min_length:
                pattern_min_length = pattern_length
            if pattern_length > pattern_max_length:
                pattern_max_length = pattern_length
            pattern_list.append(PatternGenerator.generate_pattern(pattern_length, fields, self.attributes, self.fields - 3))
        # if print flag is set, print details
        if self.print_pattern:
            TransactionGenerator._print_patterns(pattern_list)

        # change PatternTree nodes into TransactionTree nodes
        pattern_for_transaction: List[TransactionTree] = []
        for pattern in pattern_list:
            pattern_for_transaction.append(self.tree_pattern_to_transaction_tree(pattern))
        pattern_tree_indexes = {}
        for pattern in pattern_for_transaction:
            tree_indexes = []
            for _ in range(int(self.total_trees - (((len(pattern.get_nodes_list())) - pattern_min_length - 1) * (
                    (self.total_trees - self.threshold) / max(1, pattern_max_length - pattern_min_length))))):
                tree_indexes.append(random.randint(0, self.total_trees - 1))
            pattern_tree_indexes[pattern] = tree_indexes

        # Trees are generated
        tree_list: List[TransactionTree] = []
        for index in range(self.total_trees):
            chosen_patterns = []
            transaction_id = ValueGenerator.random_string()
            for pattern in pattern_for_transaction:
                for _ in range(pattern_tree_indexes[pattern].count(index)):
                    chosen_patterns.append(copy.deepcopy(pattern))
            for pattern in chosen_patterns:
                self.populate_transaction_pattern(pattern, transaction_id)
            random_nodes: List[TransactionTree] = []
            # Random nodes generation
            for _ in range(1 + int(self.avg_pattern_length + self.avg_pattern_length * len(chosen_patterns))):
                rid = ValueGenerator.random_string()
                fields_for_record: Dict[str, str] = {"tid": transaction_id, "rid": rid, "parent": None}
                for field in self.attributes:
                    field_value = self.attributes[field][random.randint(0, len(self.attributes[field]) - 1)]
                    fields_for_record[field] = field_value
                random_nodes.append(TransactionTree(fields_for_record, rid))
            random_nodes.extend(chosen_patterns)
            selected_root = random_nodes[random.randint(0, len(random_nodes) - 1)]
            root = copy.deepcopy(selected_root)
            current_tree: List[TransactionTree] = []
            if selected_root in chosen_patterns:
                current_tree.extend(root.get_nodes_list())
            else:
                current_tree.append(root)
            random_nodes.remove(selected_root)
            while len(random_nodes) > 0:
                selected_node_to_append = random_nodes[random.randint(0, len(random_nodes) - 1)]
                node_to_append = copy.deepcopy(selected_node_to_append)
                chosen_parent = current_tree[random.randint(0, len(current_tree) - 1)]
                chosen_parent.add_child(node_to_append)
                node_to_append.fields["parent"] = chosen_parent.rid
                if selected_node_to_append in chosen_patterns:
                    current_tree.extend(node_to_append.get_nodes_list())
                else:
                    current_tree.append(node_to_append)
                random_nodes.remove(selected_node_to_append)
            tree_list.append(root)
        return tree_list
