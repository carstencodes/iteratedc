#
# Copyright (c) 2021 Carsten Igel.
#
# This file is part of iteratedata_class
# (see https://github.com/carstencodes/iteratedata_class).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""Provides implementation for the visitor pattern. The NodeElement is a
   visitable element and hence accepts a NodeVisitor instance.
"""

from abc import ABC, abstractmethod
from typing import Type, Tuple, Iterable, cast
from .tree import Node


class VisitableElement(ABC):
    """Basic implementation marking an instance as visitable.
    """

    @abstractmethod
    def accept_visitor(self, visitor: "VisitorBase") -> None:
        """Accepts a visitor instance for this instance.

        Args:
            visitor (VisitorBase): The visitor to accept.
        """


class VisitorBase(ABC):
    """Basic implementation of a visitor used to visit elements.
    """

    @abstractmethod
    def visit(self, visitable: VisitableElement) -> None:
        """Performs a visit on the specified visitable element.

        Args:
            visitable (VisitableElement): The element to visit.
        """


_NodeVisitorType: Type = type(None)


class NodeElement(VisitableElement):
    """Concrete implementation of a visitable element for node elements.
    """

    def __init__(self, node: Node, parent_nodes: Iterable[Node]) -> None:
        super().__init__()
        self.__node: Node = node
        self.__parent_nodes: Tuple[Node, ...] = tuple(parent_nodes)

    @property
    def node(self) -> Node:
        """The current node represented by this instance.

        Returns:
            Node: The node.
        """
        return self.__node

    @property
    def parent_nodes(self) -> Tuple[Node, ...]:
        """The preceding nodes in the hierarchy.

        Returns:
            Tuple[Node, ...]: The nodes preceding the current nodes.
        """
        return tuple(self.__parent_nodes)

    def accept_visitor(self, visitor: VisitorBase) -> None:
        node_visitor_type: Type = globals()['_NodeVisitorType']
        if isinstance(visitor, node_visitor_type):
            node_visitor: "NodeVisitor" = cast(node_visitor_type, visitor)
            node_visitor.visit_node_element(self)


class NodeVisitor(VisitorBase, ABC):
    """Provides a basic implementation of a visitor for NodeElement
       implementations.
    """

    def visit(self, visitable: VisitableElement) -> None:
        if isinstance(visitable, NodeElement):
            node_element: NodeElement = cast(NodeElement, visitable)
            self.visit_node_element(node_element)

    @abstractmethod
    def visit_node_element(self, element: NodeElement) -> Node:
        """Called to visit a node element.

        Args:
            element (NodeElement): The element to visit.

        Returns:
            Node: The current node that has been visited.
        """

_NodeVisitorType = type(NodeVisitor)
