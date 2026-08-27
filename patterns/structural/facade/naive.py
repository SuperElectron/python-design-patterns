"""The class-shaped Facade.

Three subsystem classes, one facade whose single method performs the
sequence every caller would otherwise copy-paste.
"""

from __future__ import annotations


class Amplifier:
    def on(self) -> str:
        return "amp on"

    def set_volume(self, level: int) -> str:
        return f"volume {level}"


class Projector:
    def on(self) -> str:
        return "projector on"

    def wide_screen(self) -> str:
        return "16:9"


class Lights:
    def dim(self, percent: int) -> str:
        return f"lights {percent}%"


class HomeTheaterFacade:
    def __init__(self) -> None:
        self.amp = Amplifier()
        self.projector = Projector()
        self.lights = Lights()

    def watch_movie(self) -> list[str]:
        return [
            self.lights.dim(10),
            self.projector.on(),
            self.projector.wide_screen(),
            self.amp.on(),
            self.amp.set_volume(5),
        ]


def main() -> None:
    for step in HomeTheaterFacade().watch_movie():
        print(step)


if __name__ == "__main__":
    main()
