"""The client: renders a whole report without ever naming a format.

Everything format-specific comes from the ``DocumentFamily`` argument. Handing
in ``MARKDOWN`` or ``HTML`` (or a family of test stubs) changes every element
consistently — the renderer itself never branches on format.
"""

from __future__ import annotations

from patterns.creational.abstract_factory.examples.report_renderer.report import Report
from patterns.creational.abstract_factory.pattern import DocumentFamily


def render(family: DocumentFamily, report: Report) -> str:
    """Build the document through the family's builders only."""
    parts: list[str] = [family.heading(report.title)]
    for section in report.sections:
        parts.append(family.heading(section.title))
        parts.append(family.table(section.table.headers, section.table.rows))
        if section.note is not None:
            parts.append(family.callout(section.note))
    return "\n".join(parts)
