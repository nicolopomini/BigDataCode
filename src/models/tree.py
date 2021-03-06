from __future__ import absolute_import

from typing import Dict, List


class PatternTree:
    """
    Class that represents a pattern
    """

    def __init__(self, fields: Dict[str, str]) -> None:
        """
        Create a node that is part of a pattern
        :param fields: dict with keys the name of the fields, and values the value of each field
        Es: field: 'color', value: 'blue' means that the node contains a field 'color' = 'blue'
        """
        self.fields: Dict[str, str] = fields
        self.parent: PatternTree = None
        self.children: List[PatternTree] = []

    def add_child(self, child) -> None:
        if not isinstance(child, PatternTree):
            raise ValueError("Child must be of type 'PatternTree'")
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
        nodes_list: List[PatternTree] = [self]
        for child in self.children:
            nodes_list.extend(child.get_nodes_list())
        return nodes_list

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, PatternTree):
            return False
        return self.fields == o.fields


class TransactionTree:
    """
    Class that represents a transaction
    """

    def __init__(self, fields: Dict[str, str], rid: str) -> None:
        self.rid = rid
        self.fields = fields
        self.children: List[TransactionTree] = []
        self.parent = None

    def add_child(self, child):
        if not isinstance(child, TransactionTree):
            raise ValueError("Child must be of type 'TransactionTree'")
        self.children.append(child)
        child.fields["parent"] = self.fields["rid"]

    def print_tree(self, tabs: int = 0) -> None:
        print(self.__repr__())
        for child in self.children:
            for _ in range(tabs+1):
                print("\t", end="")
            child.print_tree(tabs + 1)

    def get_nodes_list(self) -> []:
        nodes_list: List[PatternTree] = [self]
        for child in self.children:
            nodes_list.extend(child.get_nodes_list())
        return nodes_list

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

    def __hash__(self) -> int:
        return hash(self.rid)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TransactionTree):
            return False
        return self.fields == o.fields
