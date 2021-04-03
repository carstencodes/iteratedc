#
# Copyright (c) 2021 Carsten Igel.
#
# This file is part of iteratedata_class
# (see https://github.com/carstencodes/iteratedata_class).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

from abc import ABC, abstractmethod
from typing import Type, Tuple, Iterable, cast
from .tree import Node


class VisitableElement(ABC):
    @abstractmethod
    def accept_visitor(self, visitor: "VisitorBase") -> None:
        pass


class VisitorBase(ABC):
    @abstractmethod
    def visit(self, visitable: VisitableElement) -> None:
        pass


class NodeElement(VisitableElement):
    def __init__(self, node: Node, parent_nodes: Iterable[Node]) -> None:
        super().__init__()
        self.__node: Node = node
        self.__parent_nodes: Tuple[Node, ...] = tuple(parent_nodes)

    @property
    def node(self) -> Node:
        return self.__node

    @property
    def parent_nodes(self) -> Tuple[Node, ...]:
        return tuple(self.__parent_nodes)

    def accept_visitor(self, visitor: VisitorBase) -> None:
        _node_visitor_type: Type = "NodeVisitor"
        if isinstance(visitor, _node_visitor_type):
            node_visitor: "NodeVisitor" = cast(_node_visitor_type, visitor)
            node_visitor.visit_node_element(self)


class NodeVisitor(VisitorBase):
    def visit(self, visitable: VisitableElement) -> None:
        if isinstance(visitable, NodeElement):
            node_element: NodeElement = cast(NodeElement, visitable)
            self.visit_node_element(node_element)

    @abstractmethod
    def visit_node_element(self, element: NodeElement) -> Node:
        pass
