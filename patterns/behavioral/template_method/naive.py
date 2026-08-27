"""The Gang of Four Template Method: skeleton in the base, hooks in subclasses."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Report(ABC):
    def render(self, data: dict[str, int]) -> str:
        """The template method: the skeleton nobody overrides."""
        rows = self.format_rows(data)
        return f"{self.header()}\n{rows}"

    @abstractmethod
    def header(self) -> str: ...

    @abstractmethod
    def format_rows(self, data: dict[str, int]) -> str: ...


class TextReport(Report):
    def header(self) -> str:
        return "REPORT"

    def format_rows(self, data: dict[str, int]) -> str:
        return "\n".join(f"{key}: {value}" for key, value in data.items())


class CsvReport(Report):
    def header(self) -> str:
        return "key,value"

    def format_rows(self, data: dict[str, int]) -> str:
        return "\n".join(f"{key},{value}" for key, value in data.items())


def main() -> None:
    data = {"apples": 3, "pears": 5}
    print(TextReport().render(data))
    print(CsvReport().render(data))


if __name__ == "__main__":
    main()
