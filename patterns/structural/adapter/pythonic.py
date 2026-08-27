"""Adapters at the right size.

A single-method mismatch needs a function, not a class. A wider surface can
forward wholesale with ``__getattr__`` and translate only what differs.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class FahrenheitSensor:
    """The adaptee, unchanged."""

    def get_fahrenheit(self) -> float:
        return 68.0

    def vendor_id(self) -> str:
        return "acme-42"


def celsius_reader(sensor: FahrenheitSensor) -> Callable[[], float]:
    """The one-function adapter: all the pattern that's needed here."""
    return lambda: (sensor.get_fahrenheit() - 32) * 5 / 9


class CelsiusAdapter:
    """Translate the one differing method; forward everything else."""

    def __init__(self, sensor: FahrenheitSensor) -> None:
        self._sensor = sensor

    def celsius(self) -> float:
        return (self._sensor.get_fahrenheit() - 32) * 5 / 9

    def __getattr__(self, name: str) -> Any:
        return getattr(self._sensor, name)


def main() -> None:
    read = celsius_reader(FahrenheitSensor())
    print(f"function adapter: {read():.1f} °C")
    adapter = CelsiusAdapter(FahrenheitSensor())
    print(f"class adapter:    {adapter.celsius():.1f} °C from {adapter.vendor_id()}")


if __name__ == "__main__":
    main()
