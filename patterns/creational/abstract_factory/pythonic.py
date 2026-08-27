"""What to write instead: factories are callables, families are dataclasses.

The real shape: a report renderer that must emit HTML for the web app and
Markdown for the CLI -- three builders that must stay consistent with each
other (heading, table, callout). Each family is a dataclass of callables;
the renderer never names a concrete format.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentFamily:
    """The 'complete' abstract factory: builders that belong together."""

    heading: Callable[[str], str]
    table: Callable[[list[str], list[list[str]]], str]
    callout: Callable[[str], str]


def _html_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f"<table><tr>{head}</tr>{body}</table>"


def _md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "---|" * len(headers),
        *("| " + " | ".join(row) + " |" for row in rows),
    ]
    return "\n".join(lines)


HTML = DocumentFamily(
    heading=lambda text: f"<h2>{text}</h2>",
    table=_html_table,
    callout=lambda text: f'<div class="callout">{text}</div>',
)

MARKDOWN = DocumentFamily(
    heading=lambda text: f"## {text}",
    table=_md_table,
    callout=lambda text: f"> {text}",
)


def render_sales_report(family: DocumentFamily, rows: list[list[str]]) -> str:
    """The client: builds a whole document without naming a format."""
    return "\n".join(
        [
            family.heading("Sales by region"),
            family.table(["region", "revenue"], rows),
            family.callout("Figures exclude refunds."),
        ]
    )


def main() -> None:
    rows = [["west", "$12k"], ["east", "$9k"]]
    print(render_sales_report(MARKDOWN, rows))
    print()
    print(render_sales_report(HTML, rows))


if __name__ == "__main__":
    main()
