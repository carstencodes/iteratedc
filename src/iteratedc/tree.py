#
# Copyright (c) 2021 Carsten Igel.
#
# This file is part of iteratedata_class
# (see https://github.com/carstencodes/iteratedata_class).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

"""Implementation of a raw tree structure for dataclasses including the nodes of the tree.
"""

from dataclasses import is_dataclass, fields, Field, asdict
from typing import (
    Iterable,
    Iterator,
    List,
    Optional,
    Type,
    Any,
    Tuple,
    NamedTuple,
    Mapping,
    get_args,
)
from collections.abc import Iterable as _Iterable_Collection


class _FieldValueWithMetaData(NamedTuple):
    value: Any
    corresponding_field: Optional[Field] = None
    field_index: Optional[int] = None


def _is_generic_collection_type(type_to_check: Type) -> bool:
    has_origin: bool = hasattr(type_to_check, "__origin__")
    if not has_origin:
        return False

    origin: Type = type_to_check.__origin__

    return (
        issubclass(origin, _Iterable_Collection)
        and len(get_args(type_to_check)) > 0
    )


def _iterate_over_current_item(
    data_class: Any,
) -> Iterator[_FieldValueWithMetaData]:
    if data_class is None or not is_dataclass(data_class):
        yield from []

    else:
        flds: Tuple[Field, ...] = fields(data_class)
        data_class_value: Mapping[str, Any] = asdict(data_class)
        for fld in flds:
            if is_dataclass(fld.type):
                yield _FieldValueWithMetaData(
                    data_class_value[fld.name], fld, None
                )

        for fld in flds:
            if _is_generic_collection_type(fld.type):
                args: Tuple[Type, ...] = get_args(fld.type)
                if len(args) > 1:
                    # Cannot iterate over multiple items in this stage
                    continue
                type_arg: Type = args[0]
                if is_dataclass(type_arg):
                    items: Iterable[Any] = data_class_value[fld.name]
                    i = 0
                    for item in items:
                        i = i + 1
                        yield _FieldValueWithMetaData(item, fld, i)


class Node:
    """Implementation of a tree node for dataclass members.
    """

    def __init__(
        self,
        value: _FieldValueWithMetaData,
        children: Optional[Iterable["Node"]] = None,
    ) -> None:
        self.__field = value
        self.__children = list(children or [])

    @property
    def item(self) -> Any:
        """The field instance.

        Returns:
            Any: The current instance of the field.
        """
        return self.__field.value

    @property
    def item_index(self) -> Optional[int]:
        """The index in a parent collection represented by the field.

        Returns:
            Optional[int]: The index or None, if the field is no collection.
        """
        return self.__field.field_index

    @property
    def meta_data(self) -> Mapping[str, Any]:
        """Gets the meta data of the field.

        Returns:
            Mapping[str, Any]: A mapping of field meta data values.
        """
        fld: Optional[Field] = self.__field.corresponding_field
        if fld is None:
            return {}

        return fld.metadata

    @property
    def name(self) -> str:
        """The name of the field.

        Returns:
            str: The name of the field. Might be empty.
        """
        fld: Optional[Field] = self.__field.corresponding_field
        if fld is None:
            return ""

        return fld.name

    @property
    def type(self) -> Type:
        """The type of the current value.

        Returns:
            Type: The type of the current value.
        """
        fld: Optional[Field] = self.__field.corresponding_field
        if fld is None or self.item_index is not None:
            return type(self.item)

        return fld.type

    @property
    def children(self) -> Iterable["Node"]:
        """The child nodes.

        Returns:
            [type]: The nodes following the current node.
        """
        return self.__children


class Tree:
    """Implements a tree as a sequence of nodes.
    """

    def __init__(self, root: Node) -> None:
        self.__root = root

    @property
    def root(self) -> Node:
        """The root node of the tree.

        Returns:
            Node: The root node.
        """
        return self.__root


def _create_node_from_item(field_with_meta: _FieldValueWithMetaData) -> Node:

    if field_with_meta is None:
        raise ValueError(field_with_meta, " must not be None")

    data_class: Any = field_with_meta.value

    if not is_dataclass(data_class):
        raise ValueError(data_class, " must be a data class")

    child_nodes: List[Node] = []
    for meta_field in _iterate_over_current_item(data_class):
        node: Node = _create_node_from_item(meta_field)
        child_nodes.append(node)

    node: Node = Node(field_with_meta, child_nodes)
    return node


def create_tree_from_dataclass(data_class: Any) -> Optional[Tree]:
    """Takes the specified dataclass and transforms it to a tree.

    Args:
        data_class (Any): The data class to analyze.

    Returns:
        Optional[Tree]: The tree. If the argument is None
                        or no dataclass, the result will be None.
    """
    if data_class is None or not is_dataclass(data_class):
        return None

    meta_root_node: _FieldValueWithMetaData = _FieldValueWithMetaData(
        data_class, None, None
    )
    node: Node = _create_node_from_item(meta_root_node)
    return Tree(node)
