"""Global objects the stdlib ships.

``math.pi``: the Constant Pattern. ``calendar.day_name``: an import-time
built global object. ``os.environ``: the rare mutable global whose mutation
is its documented job.
"""

from __future__ import annotations

import calendar
import math
import os


def midweek_day() -> str:
    return str(calendar.day_name[2])


def circle_area(radius: float) -> float:
    return math.pi * radius**2


def with_temp_env(key: str, value: str) -> str:
    """os.environ is mutable by design; clean up what you touch."""
    os.environ[key] = value
    try:
        return os.environ[key]
    finally:
        del os.environ[key]


def main() -> None:
    print(f"constant pattern: math.pi = {math.pi}")
    print(f"global object:    day_name[2] = {midweek_day()}")
    print(f"mutable global:   {with_temp_env('DEMO_KEY', 'demo')}")


if __name__ == "__main__":
    main()
