#
# Copyright (c) 2021 Carsten Igel.
#
# This file is part of iteratedata_class
# (see https://github.com/carstencodes/iteratedata_class).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

import iteratedc
import unittest

from dataclasses import dataclass, field

@dataclass
class Simple:
    a: int = field()
    b: int = field()
    c: int = field()


class BasicTest(unittest.TestCase):
    def test_sample(self) -> None:
        simple: Simple = Simple(1, 2, 3)
        items = iteratedc.flatten_hierarchy(simple)
        self.assertEqual(len(items), 1)


if __name__ == "__main__":
    unittest.main()
