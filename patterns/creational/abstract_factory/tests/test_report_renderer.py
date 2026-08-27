"""Behavioral tests for the report-renderer mini-project."""

from __future__ import annotations

from patterns.creational.abstract_factory.examples.report_renderer.main import Q3
from patterns.creational.abstract_factory.examples.report_renderer.renderer import render
from patterns.creational.abstract_factory.examples.report_renderer.report import (
    Report,
    Section,
    Table,
)
from patterns.creational.abstract_factory.pattern import HTML, MARKDOWN
from patterns.creational.abstract_factory.tests.test_family import make_recording_family

REPORT = Report(
    title="Weekly",
    sections=(
        Section(
            title="Sales",
            table=Table(("region", "revenue"), (("west", "$12k"),)),
            note="Excludes refunds.",
        ),
    ),
)


class TestRenderer:
    def test_same_report_both_families_same_content(self) -> None:
        md = render(MARKDOWN, REPORT)
        html = render(HTML, REPORT)
        for content in ("Weekly", "Sales", "west", "$12k", "Excludes refunds."):
            assert content in md
            assert content in html

    def test_family_controls_every_element_consistently(self) -> None:
        html = render(HTML, REPORT)
        assert "<h2>Weekly</h2>" in html
        assert "<td>west</td>" in html
        assert '<div class="callout">Excludes refunds.</div>' in html
        assert "##" not in html  # no other family's markup leaks in

    def test_note_is_optional(self) -> None:
        bare = Report("R", (Section("S", Table(("h",), (("v",),))),))
        assert "callout" not in render(HTML, bare)

    def test_client_is_family_agnostic(self) -> None:
        """A recording stub family sees exactly the calls the report implies."""
        calls: list[str] = []
        render(make_recording_family(calls), Q3)
        # Q3: report heading + 2 section headings, 2 tables, 1 callout
        assert calls.count("heading") == 3
        assert calls.count("table") == 2
        assert calls.count("callout") == 1
