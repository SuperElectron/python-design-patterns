"""Demo: one quarterly report through two document families."""

from __future__ import annotations

from patterns.creational.abstract_factory.examples.report_renderer.renderer import render
from patterns.creational.abstract_factory.examples.report_renderer.report import (
    Report,
    Section,
    Table,
)
from patterns.creational.abstract_factory.pattern import HTML, MARKDOWN

Q3 = Report(
    title="Q3 review",
    sections=(
        Section(
            title="Sales by region",
            table=Table(("region", "revenue"), (("west", "$12k"), ("east", "$9k"))),
            note="Figures exclude refunds.",
        ),
        Section(
            title="Support load",
            table=Table(("tier", "tickets"), (("helpdesk", "214"), ("on-call", "37"))),
        ),
    ),
)


def main() -> None:
    print("--- Markdown (CLI) ---")
    print(render(MARKDOWN, Q3))
    print("--- HTML (web) ---")
    print(render(HTML, Q3))


if __name__ == "__main__":
    main()
