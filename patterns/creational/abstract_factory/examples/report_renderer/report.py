"""Domain types for the report-renderer mini-project."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Table:
    """Tabular data, format-agnostic."""

    headers: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class Section:
    """One titled block of the report, with an optional callout note."""

    title: str
    table: Table
    note: str | None = None


@dataclass(frozen=True)
class Report:
    """A whole report: a title and its sections."""

    title: str
    sections: tuple[Section, ...]
