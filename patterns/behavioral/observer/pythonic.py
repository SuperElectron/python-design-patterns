"""Observers as callables; observation hidden behind a property.

Subscribing is appending a function. The property setter shows the idiom
most Python APIs actually use: plain assignment triggers the broadcast.
"""

from __future__ import annotations

from collections.abc import Callable

Listener = Callable[[float], None]


class WeatherStation:
    def __init__(self) -> None:
        self.listeners: list[Listener] = []
        self._temperature = 0.0

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        self._temperature = value
        for listen in list(self.listeners):  # copy: observers may unsubscribe
            listen(value)


def main() -> None:
    station = WeatherStation()
    seen: list[float] = []
    alerts: list[float] = []
    station.listeners.append(seen.append)
    station.listeners.append(lambda t: alerts.append(t) if t > 30 else None)

    station.temperature = 21.5  # plain assignment broadcasts
    station.temperature = 35.0
    print(f"seen: {seen}, alerts: {alerts}")


if __name__ == "__main__":
    main()
