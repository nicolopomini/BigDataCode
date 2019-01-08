from __future__ import absolute_import

from typing import Dict, List


class TreePattern:
    def __init__(self, fields: Dict[str, str]) -> None:
        """
        Create a node that is part of a pattern
        :param fields: dict with keys the name of the fields, and values the value of each field
        Es: field: 'color', value: 'blue' means that the node contains a field 'color' = 'blue'
        """
        self.fields: Dict[str, str] = fields
        self.parent: TreePattern = None
        self.children: List[TreePattern] = []

    def add_child(self, child) -> None:
        if not isinstance(child, TreePattern):
            raise ValueError("Child must be of type 'TreePattern'")
        self.children.append(child)
        child.parent = self

    def __repr__(self) -> str:
        length = len(self.fields)
        i = 1
        s = "Node("
        if length == 0:
            s += "<Anything>"
        else:
            for f in self.fields:
                s += "'%s' = %s" % (f, self.fields[f])
                if i < length:
                    s += ", "
                i += 1
        s += ")"
        return s

    def print_tree(self, tabs: int = 0) -> None:
        print(self.__repr__())
        for child in self.children:
            for _ in range(tabs+1):
                print("\t", end="")
            child.print_tree(tabs + 1)

    def get_nodes_list(self) -> []:
        nodes_list: List[TreePattern] = [self]
        for child in self.children:
            nodes_list.extend(child.get_nodes_list())
        return nodes_list

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TreePattern):
            return False
        return self.fields == o.fields


class TransactionTree:
    def __init__(self, fields: Dict[str, str]) -> None:
        self.fields = fields
        self.parent: TransactionTree = None
        self.children: List[TransactionTree] = []

    def add_child(self, child):
        if not isinstance(child, TransactionTree):
            raise ValueError("Child must be of type 'TransactionTree'")
        self.children.append(child)
        child.parent = self
