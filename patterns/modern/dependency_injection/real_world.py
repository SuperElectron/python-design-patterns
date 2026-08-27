"""The stdlib does DI by keyword argument.

``sorted(key=...)`` injects the ordering; ``json.dumps(cls=...)`` injects
the encoder. Same seam, same benefit.
"""

from __future__ import annotations

import json
from typing import Any


class UpperEncoder(json.JSONEncoder):
    def encode(self, o: Any) -> str:
        return super().encode(o).upper()


def sort_by_injected_policy(words: list[str]) -> list[str]:
    return sorted(words, key=str.casefold)


def dump_with_injected_encoder(data: dict[str, str]) -> str:
    return json.dumps(data, cls=UpperEncoder)


def main() -> None:
    print(sort_by_injected_policy(["b", "A", "c"]))
    print(dump_with_injected_encoder({"k": "v"}))


if __name__ == "__main__":
    main()
