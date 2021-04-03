#
# Copyright (c) 2021 Carsten Igel.
#
# This file is part of iteratedc
# (see https://github.com/carstencodes/iteratedc).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

from typing import Any, Iterable, Iterator, List
from .tree import Node
from .visitor import NodeElement
from .iterators import DataClassIterable, IterationMode


def iterate_over_data_class(
    dataclass: Any, mode: IterationMode = IterationMode.BreadthFirstSearch
) -> Iterator[NodeElement]:
    return iter(DataClassIterable(mode, dataclass))


def iterate_over_data_classes(
    dataclasses: Iterable[Any],
    mode: IterationMode = IterationMode.BreadthFirstSearch,
) -> Iterator[NodeElement]:
    return iter(DataClassIterable(mode, dataclasses))


def flatten_hierarchy(
    dataclass: Any, mode: IterationMode = IterationMode.BreadthFirstSearch
) -> List[NodeElement]:
    result: List[NodeElement] = []
    nodes: Iterator[NodeElement] = iterate_over_data_class(dataclass, mode)
    try:
        while True:
            result.append(next(nodes))
    except StopIteration:
        return result
