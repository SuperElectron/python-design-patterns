"""Abstract Factory as Python actually keeps it: a family of callables.

The classic pattern exists so client code can build related objects without
naming their classes. In Python, factories are just callables, and a *family*
of factories that must stay consistent with each other is a frozen dataclass
bundling them. ``DocumentFamily`` is that bundle for document rendering:
swap the family and every element the client builds changes format together.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentFamily:
    """A consistent set of document builders — the whole abstract factory.

    Clients accept a ``DocumentFamily`` and never name a concrete format;
    frozen so a family cannot drift into a mixed one after construction.
    """

    heading: Callable[[str], str]
    table: Callable[[Sequence[str], Sequence[Sequence[str]]], str]
    callout: Callable[[str], str]


def _html_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f"<table><tr>{head}</tr>{body}</table>"


def _md_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
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
