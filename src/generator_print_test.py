from __future__ import absolute_import

from tree_for_generator import Pattern
from values import ValueGenerator
from src import Gen

g = Gen(100, 20, 3, 10)
treelist = g.generate_data()
for tree in treelist:
    tree.print_tree()
    print()