"""Behavioral tests for the DocumentFamily building block."""

from __future__ import annotations

import dataclasses
from collections.abc import Sequence

import pytest

from patterns.creational.abstract_factory import HTML, MARKDOWN, DocumentFamily

HEADERS = ["region", "revenue"]
ROWS = [["west", "$12k"], ["east", "$9k"]]


class TestFamilies:
    def test_markdown_family_agrees_with_itself(self) -> None:
        assert MARKDOWN.heading("Sales") == "## Sales"
        table = MARKDOWN.table(HEADERS, ROWS)
        assert table.splitlines()[0] == "| region | revenue |"
        assert "| west | $12k |" in table
        assert MARKDOWN.callout("note") == "> note"

    def test_html_family_agrees_with_itself(self) -> None:
        assert HTML.heading("Sales") == "<h2>Sales</h2>"
        table = HTML.table(HEADERS, ROWS)
        assert table.startswith("<table>")
        assert "<td>west</td>" in table
        assert HTML.callout("note") == '<div class="callout">note</div>'

    def test_every_row_survives_in_both_families(self) -> None:
        for family in (MARKDOWN, HTML):
            table = family.table(HEADERS, ROWS)
            for cell in ("west", "$12k", "east", "$9k"):
                assert cell in table


def make_recording_family(calls: list[str]) -> DocumentFamily:
    """A stub family whose builders record what the client asks for."""

    def heading(text: str) -> str:
        calls.append("heading")
        return f"H({text})"

    def table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
        calls.append("table")
        return "T"

    def callout(text: str) -> str:
        calls.append("callout")
        return "C"

    return DocumentFamily(heading=heading, table=table, callout=callout)


class TestFamilyDiscipline:
    def test_families_are_frozen(self) -> None:
        with pytest.raises(dataclasses.FrozenInstanceError):
            MARKDOWN.heading = HTML.heading  # type: ignore[misc]

    def test_replace_derives_a_consistent_variant(self) -> None:
        plain = dataclasses.replace(HTML, callout=lambda text: f"<p>{text}</p>")
        assert plain.callout("note") == "<p>note</p>"
        assert plain.heading("Sales") == HTML.heading("Sales")  # rest shared

    def test_markdown_table_carries_the_separator_row(self) -> None:
        table = MARKDOWN.table(["region", "total"], [["west", "1280"]])
        lines = table.splitlines()
        assert lines[0] == "| region | total |"
        assert lines[1] == "|---|---|"  # without it, the table is not Markdown
        assert lines[2] == "| west | 1280 |"
