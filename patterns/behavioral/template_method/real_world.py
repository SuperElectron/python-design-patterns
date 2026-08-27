"""``json.JSONEncoder``: a template method you override in the wild.

encode() owns the skeleton; the default() hook is called exactly at the
step the skeleton cannot handle itself.
"""

from __future__ import annotations

import json
from datetime import date
from typing import Any


class DateAwareEncoder(json.JSONEncoder):
    """Override the one hook; inherit the whole encoding skeleton."""

    def default(self, o: Any) -> Any:
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)


def dump_event(event: dict[str, object]) -> str:
    return json.dumps(event, cls=DateAwareEncoder, sort_keys=True)


def main() -> None:
    print(dump_event({"name": "launch", "when": date(2026, 8, 26)}))


if __name__ == "__main__":
    main()
