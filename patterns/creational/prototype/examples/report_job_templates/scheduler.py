"""A scheduler stamping out report jobs from preconfigured templates.

``functools.partial`` freezes each template's settings into a zero-argument
factory registered on a ``TemplateRegistry``; per-run tweaks come from the
registry's ``create(**overrides)`` (``dataclasses.replace`` underneath), so a
rushed run never touches the template it came from.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial

from patterns.creational.prototype.examples.report_job_templates.models import ReportJob
from patterns.creational.prototype.pattern import TemplateRegistry


def build_template_menu() -> TemplateRegistry[ReportJob]:
    menu: TemplateRegistry[ReportJob] = TemplateRegistry()
    menu.register(
        "nightly-sales",
        partial(
            ReportJob,
            name="nightly-sales",
            query="SELECT * FROM sales WHERE day = today()",
            recipients=("sales-leads@example.com",),
            filters=("exclude-test-accounts",),
        ),
    )
    menu.register(
        "weekly-audit",
        partial(
            ReportJob,
            name="weekly-audit",
            query="SELECT * FROM ledger WHERE week = this_week()",
            recipients=("finance@example.com", "cfo@example.com"),
            fmt="xlsx",
        ),
    )
    return menu


@dataclass
class Scheduler:
    """Queues fresh jobs stamped from the menu."""

    menu: TemplateRegistry[ReportJob] = field(default_factory=build_template_menu)
    queue: list[ReportJob] = field(default_factory=list)

    def enqueue(self, template: str, **overrides: object) -> ReportJob:
        job = self.menu.create(template, **overrides)
        self.queue.append(job)
        return job
