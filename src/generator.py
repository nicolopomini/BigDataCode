from __future__ import absolute_import

from typing import List

from tree import TreePattern
from tree import Pattern
from values import ValueGenerator
import random
import copy
import math


class Gen:
    def __init__(self, total_trees: int, total_patterns: int, min_pattern_length: int, max_pattern_length: int) -> None:
        """
        Create a node that is part of a pattern
        :param total_trees: the total number of trees that will be generated
        :param total_patterns: the total number of patterns that will be used
        :param min_pattern_length the minimum number of edges a pattern must have
        :param max_pattern_length the maximum number of edges a pattern can have (must be smaller than max_nodes)
        """
        if total_trees < 1:
            raise ValueError("There must be at least one tree. Given %d" % total_trees)
        if min_pattern_length < 1:
            raise ValueError("There must be at least 2 nodes in a pattern. Given %d" % min_pattern_length)
        if min_pattern_length > max_pattern_length:
            raise ValueError("The minimum number of nodes in each pattern must be "
                             "smaller than the maximum number of nodes in each pattern. "
                             "Given min_pattern_length %d and max_pattern_length %d" % (min_pattern_length, max_pattern_length))
        self.total_patterns: int = total_patterns
        self.total_trees: int = total_trees
        self.min_pattern_nodes: int = min_pattern_length
        self.max_pattern_nodes: int = max_pattern_length

    def generate_data(self) -> []:
        # Patterns are generated
        fields = 100
        vals = 100
        pattern_list: List[TreePattern] = []
        for _ in range(self.total_patterns):
            attributes = ValueGenerator.generate_pattern_values(fields, vals)
            pattern_list.append(Pattern.generate_pattern(random.randint(self.min_pattern_nodes, self.max_pattern_nodes), [field for field in attributes], attributes))
        # Tree indexes for patterns are generated
        pattern_tree_indexes = {}
        for pattern in pattern_list:
            tree_indexes = []
            min_frequency = (self.total_trees / 100) * 20;
            for _ in range(math.floor(self.total_trees - (((len(pattern.get_nodes_list()) - 1) - self.min_pattern_nodes) * ((self.total_trees - min_frequency) / (self.max_pattern_nodes - self.min_pattern_nodes))))):
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
