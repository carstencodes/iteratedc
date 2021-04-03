# iteratedc - A small python iterator for python 3 dataclasses

`iteratedc` is a small library used to iterate over python 3 dataclasses. It will not only traverse the low level, but will create the a tree-search diving down collections of dataclasses as well. If on each level, a dataclass is present it will follow these child nodes one level down.

You can choose between four operation modes:

* BFS (Breadth first search)
* DFS (Depth first search)
  * Pre-Order
  * In-Order
  * Post-Order
  * Reverse Pre-Order
  * Reverse Post-Order

The result will not be the current node but a NodeElement carrying the current node.

These `NodeElement`s accept visitors according to the visitor pattern.

## Licensing

This library is published under BSD-3-Clause license.

## Versioning

This library follows semantic versioning 2.0. Any breaking change will produce a new major release. Versions below 1.0 are considered to have a unstable interface.
