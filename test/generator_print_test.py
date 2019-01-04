from __future__ import absolute_import

from generator import Gen
from tree import Pattern
from values import ValueGenerator


g = Gen(200, 30, 1, 10)
treelist = g.generate_data()
for tree in treelist:
    tree.print_tree()
    print()