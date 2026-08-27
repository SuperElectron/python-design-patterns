"""The Gang of Four object adapter, translated literally.

The adapter implements the target interface and holds the adaptee,
translating call by call.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class FahrenheitSensor:
    """The adaptee: a class we cannot edit, with the wrong interface."""

    def get_fahrenheit(self) -> float:
        return 68.0


class Thermometer(ABC):
    """The target interface our code is written against."""

    @abstractmethod
    def celsius(self) -> float: ...


class SensorAdapter(Thermometer):
    def __init__(self, sensor: FahrenheitSensor) -> None:
        self._sensor = sensor

    def celsius(self) -> float:
        return (self._sensor.get_fahrenheit() - 32) * 5 / 9


def describe(thermometer: Thermometer) -> str:
    return f"{thermometer.celsius():.1f} °C"


def main() -> None:
    print(describe(SensorAdapter(FahrenheitSensor())))


if __name__ == "__main__":
    main()
