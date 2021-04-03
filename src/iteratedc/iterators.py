#
# Copyright (c) 2021 Carsten Igel.
#
# This file is part of iteratedc
# (see https://github.com/carstencodes/iteratedc).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""Contains all functions and classes required for iterating over a hierarchy
   of data classes. The data class will be transformed to a tree, whose nodes
   will be iterated.
"""

from dataclasses import field, dataclass
from abc import ABC, abstractmethod
from typing import (
    Iterable,
    Iterator,
    Optional,
    TypeVar,
    Generic,
    Set,
    Union,
    Tuple,
    List,
)
from collections import deque
from enum import Enum, auto
from sys import version_info

from .tree import Tree, Node, create_tree_from_dataclass
from .visitor import NodeElement


_DO_NOT_ITERATE_OVER_NODE_: str = "iteratedc_skip"


if version_info.major == 3 and version_info.minor <= 8:
    from typing import Deque  # pylint: disable=C0412
else:
    Deque = deque


DataClassType: TypeVar = TypeVar("DataClassType")


@dataclass
class _RootNode:
    nodes: Iterable[str] = field(metadata={_DO_NOT_ITERATE_OVER_NODE_: True})


_DataClassNodeType = Union[_RootNode, DataClassType]


class IterationMode(Enum):
    """Represents the mode of operation to use for tree traversal.
    """

    BREAD_FIRST_SEARCH = auto()
    """Use BFS tree iteration
    """
    PRE_ORDER_DEPTH_FIRST_SEARCH = auto()
    """Use Pre-Order DFS tree iteration.
    """
    POST_ORDER_DEPTH_FIRST_SEARCH = auto()
    """Use Post-Order DFS tree iteration.
    """
    REVERSE_PRE_ORDER_DEPTH_FIRST_SEARCH = auto()
    """Use reverse Pre-Order DFS tree iteration.
    """
    REVERSE_POST_ORDER_DEPTH_FIRST_SEARCH = auto()
    """Use reverse Post-Order DFS tree iteration.
    """


OrderedNodeCollection = Deque[Tuple[Node, Deque[Node]]]


class _DataClassIteratorBase(ABC):  # pylint: disable=R0903
    def __init__(self, tree: Tree) -> None:
        super().__init__()
        if tree is None:
            raise ValueError(tree, " must not be none")

        self.__tree: Tree = tree
        self.__node_element_iterator: Optional[Iterator[NodeElement]] = None

    @property
    def _tree(self) -> Tree:
        return self.__tree

    def __next__(self) -> NodeElement:
        if self.__node_element_iterator is None:
            elements: Iterable[NodeElement] = self.__build()
            self.__node_element_iterator = iter(elements)

        return next(self.__node_element_iterator)

    @abstractmethod
    def _build_ordered_node_collection(self) -> OrderedNodeCollection:
        pass

    def __build(self) -> Iterable[NodeElement]:
        items: List[NodeElement] = []

        ordered_raw_items: OrderedNodeCollection = self._build_ordered_node_collection()

        for item in ordered_raw_items:
            node, parent_nodes = item
            items.append(NodeElement(node, parent_nodes))

        return items


class _BreathFirstDataClassIterator(_DataClassIteratorBase):
    def _build_ordered_node_collection(self) -> OrderedNodeCollection:
        result: OrderedNodeCollection = deque()
        nodes_to_traverse: OrderedNodeCollection = deque()
        visited: Set[Node] = set()

        nodes_to_traverse.append((self._tree.root, deque()))

        while len(nodes_to_traverse) > 0:
            current, stack = nodes_to_traverse.popleft()
            if current not in visited:
                visited.add(current)
                result.append((current, stack))
                next_stack: Deque[Node] = deque(stack)
                next_stack.append(current)
                nodes_to_traverse.extend(
                    [(c, next_stack) for c in current.children]
                )

        return result


class _PostOrderDepthFirstDataClassIterator(_DataClassIteratorBase):
    def __init__(self, tree: Tree, reverse: bool) -> None:
        super().__init__(tree)
        self.__reverse = reverse

    def _build_ordered_node_collection(self) -> OrderedNodeCollection:
        result: OrderedNodeCollection = _PostOrderDepthFirstDataClassIterator._build_queue(
            self._tree.root, deque(), set()
        )

        if not self.__reverse:
            return result

        result.reverse()
        return result

    @staticmethod
    def _build_queue(
        node: Node, stack: Deque[Node], visited: Set[Node]
    ) -> OrderedNodeCollection:
        if not node in visited:
            visited.add(node)
            result: OrderedNodeCollection = deque()
            stack.append(node)
            for child in node.children:
                next_items = _PostOrderDepthFirstDataClassIterator._build_queue(
                    child, stack, visited
                )
                result.extend(next_items)
            stack.pop(node)
            result.append((node, deque(stack)))

        return deque()


class _PreOrderDepthFirstDataClassIterator(_DataClassIteratorBase):
    def __init__(self, tree: Tree, reverse: bool) -> None:
        super().__init__(tree)
        self.__reverse = reverse

    def _build_ordered_node_collection(self) -> OrderedNodeCollection:
        result: OrderedNodeCollection = _PreOrderDepthFirstDataClassIterator._build_queue(
            self._tree.root, deque(), set()
        )

        if not self.__reverse:
            return result

        result.reverse()
        return result

    @staticmethod
    def _build_queue(
        node: Node, stack: Deque[Node], visited: Set[Node]
    ) -> OrderedNodeCollection:
        if not node in visited:
            visited.add(node)
            result: OrderedNodeCollection = deque()
            result.append((node, deque(stack)))
            stack.append(node)
            for child in node.children:
                next_items = _PreOrderDepthFirstDataClassIterator._build_queue(
                    child, stack, visited
                )
                result.extend(next_items)
            stack.pop(node)

        return deque()


class DataClassIterable(Generic[DataClassType]):
    """Class transforming a dataclass into an iterable of NodeElements
    """

    def __init__(self, mode: IterationMode, *args: DataClassType) -> None:
        super().__init__()

        work_tree: _DataClassNodeType = args[0] if len(
            args
        ) == 1 else _RootNode(args)
        tree: Optional[Tree] = create_tree_from_dataclass(work_tree)
        if tree is None:
            raise ValueError(args, " must be a dataclass")

        self.__tree: Tree = tree

        if mode in IterationMode:
            self.__mode = mode
        else:
            raise ValueError("Not a valid IterationMode")

    def __iter__(self) -> Iterator[NodeElement]:
        iterator: _DataClassIteratorBase

        if IterationMode.BREAD_FIRST_SEARCH == self.__mode:
            iterator = _BreathFirstDataClassIterator(self.__tree)
        elif IterationMode.POST_ORDER_DEPTH_FIRST_SEARCH == self.__mode:
            iterator = _PostOrderDepthFirstDataClassIterator(
                self.__tree, False
            )
        elif IterationMode.PRE_ORDER_DEPTH_FIRST_SEARCH == self.__mode:
            iterator = _PreOrderDepthFirstDataClassIterator(self.__tree, False)
        elif (
            IterationMode.REVERSE_POST_ORDER_DEPTH_FIRST_SEARCH == self.__mode
        ):
            iterator = _PostOrderDepthFirstDataClassIterator(self.__tree, True)
        elif IterationMode.REVERSE_PRE_ORDER_DEPTH_FIRST_SEARCH == self.__mode:
            iterator = _PreOrderDepthFirstDataClassIterator(self.__tree, True)
        else:
            raise NotImplementedError(self.__mode)  # Heuristically unreachable

        return iterator
