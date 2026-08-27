"""``pickle``: mementos that survive the process.

dumps() produces an opaque snapshot; loads() restores an equivalent object
-- checkpoint/rollback for anything picklable.
"""

from __future__ import annotations

import pickle
from dataclasses import dataclass, field


@dataclass
class Game:
    level: int = 1
    inventory: list[str] = field(default_factory=list)


def checkpoint(game: Game) -> bytes:
    return pickle.dumps(game)


def rollback(snapshot: bytes) -> Game:
    restored = pickle.loads(snapshot)
    assert isinstance(restored, Game)
    return restored


def main() -> None:
    game = Game()
    game.inventory.append("sword")
    save = checkpoint(game)
    game.level, game.inventory = 9, []
    print(f"after disaster: {game}")
    print(f"rolled back:    {rollback(save)}")


if __name__ == "__main__":
    main()
