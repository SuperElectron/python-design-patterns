"""The Gang of Four Observer: Subject, Observer ABC, update()."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float) -> None: ...


class Display(Observer):
    def __init__(self) -> None:
        self.shown: float | None = None

    def update(self, temperature: float) -> None:
        self.shown = temperature


class AlarmLog(Observer):
    def __init__(self, threshold: float) -> None:
        self.threshold = threshold
        self.alerts: list[float] = []

    def update(self, temperature: float) -> None:
        if temperature > self.threshold:
            self.alerts.append(temperature)


class WeatherStation:
    """The subject."""

    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self._temperature = 0.0

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def set_temperature(self, value: float) -> None:
        self._temperature = value
        for observer in self._observers:
            observer.update(value)


def main() -> None:
    station, display, alarm = WeatherStation(), Display(), AlarmLog(30.0)
    station.attach(display)
    station.attach(alarm)
    station.set_temperature(21.5)
    station.set_temperature(35.0)
    print(f"display shows {display.shown}, alarms: {alarm.alerts}")


if __name__ == "__main__":
    main()
