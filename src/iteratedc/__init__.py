#
# Copyright (c) 2021 Carsten Igel.
#
# This file is part of iteratedc
# (see https://github.com/carstencodes/iteratedc).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""iteratedc is set of function for analyzing an object hierarchy
   of python 3 dataclasses. As a result an iterator is returned.
   Each dataclass of the hierarchy will be represented by a NodeElement
   instance that holds the current instance, metadata and the position
   in the hierarchy.
"""

from typing import Any, Iterable, Iterator, List
from .tree import Node
from .visitor import NodeElement, NodeVisitor
from .iterators import DataClassIterable, IterationMode


def iterate_over_data_class(
    dataclass: Any, mode: IterationMode = IterationMode.BREAD_FIRST_SEARCH
) -> Iterator[NodeElement]:
    """Creates an iterator over the specified dataclass returning all
       dataclasses in the hierarchy using the specified tree iteration mode.

    Args:
        dataclass (Any): The value to traverse. Must be a dataclass.
        mode (IterationMode, optional): The mode of operation to use for iteration.
                                        Defaults to IterationMode.BREAD_FIRST_SEARCH.

    Returns:
        Iterator[NodeElement]: The iterator over the sequence of NodeElements

    Yields:
        Iterator[NodeElement]: The node elements over a list of ordered NodeElements
    """
    return iter(DataClassIterable(mode, dataclass))


def iterate_over_data_classes(
    dataclasses: Iterable[Any],
    mode: IterationMode = IterationMode.BREAD_FIRST_SEARCH,
) -> Iterator[NodeElement]:
    """Creates an iterator over the specified dataclasses returning all
       dataclasses in the hierarchy using the specified tree iteration mode.

    Args:
        dataclass (Iterable[Any]): The values to traverse. Any instance
                                   must be a dataclass.
        mode (IterationMode, optional): The mode of operation to use for
                                        iteration. Defaults to IterationMode.BREAD_FIRST_SEARCH.

    Returns:
        Iterator[NodeElement]: The iterator over the sequence of NodeElements

    Yields:
        Iterator[NodeElement]: The node elements over a list of ordered NodeElements
    """
    return iter(DataClassIterable(mode, dataclasses))


def flatten_hierarchy(
    dataclass: Any, mode: IterationMode = IterationMode.BREAD_FIRST_SEARCH
) -> List[NodeElement]:
    """Creates a list of NodeElements from the specified dataclass ordered for
       a tree traversal using the specified tree iteration mode.

    Args:
        dataclass (Any): The value to traverse. Must be a data class.
        mode (IterationMode, optional): The mode of traversal. Defaults
                                        to IterationMode.BREAD_FIRST_SEARCH.

    Returns:
        List[NodeElement]: The list of NodeElements.
    """
    result: List[NodeElement] = []
    nodes: Iterator[NodeElement] = iterate_over_data_class(dataclass, mode)
    try:
        while True:
            result.append(next(nodes))
    except StopIteration:
        return result
