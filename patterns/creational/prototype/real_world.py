"""The stdlib's clone operation: the ``copy`` module.

``copy.copy`` is a shallow clone (nested mutables are shared);
``copy.deepcopy`` clones the whole object graph. Classes customize both via
the ``__copy__`` / ``__deepcopy__`` protocol -- the Prototype pattern as a
language protocol.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field


@dataclass
class Board:
    name: str
    tiles: list[list[int]] = field(default_factory=lambda: [[0, 0], [0, 0]])


def shallow_shares_nested_state(template: Board) -> bool:
    clone = copy.copy(template)
    clone.tiles[0][0] = 9
    return template.tiles[0][0] == 9  # the nested list is shared!


def deep_is_independent(template: Board) -> bool:
    clone = copy.deepcopy(template)
    clone.tiles[0][0] = 9
    return template.tiles[0][0] == 0


def main() -> None:
    print(f"shallow copy shares nested state: {shallow_shares_nested_state(Board('a'))}")
    print(f"deep copy is independent:         {deep_is_independent(Board('b'))}")


if __name__ == "__main__":
    main()
