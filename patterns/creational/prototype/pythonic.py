"""What to write instead: a registry of callables.

The real shape: a scheduler stamping out report jobs from preconfigured
templates. ``functools.partial`` freezes each template's settings into a
zero-argument factory; per-run tweaks come from ``dataclasses.replace`` on
the frozen product -- no clone() protocol anywhere.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, replace
from functools import partial


@dataclass(frozen=True)
class ReportJob:
    name: str
    query: str
    recipients: tuple[str, ...]
    fmt: str = "pdf"
    filters: tuple[str, ...] = ()


TEMPLATES: dict[str, Callable[[], ReportJob]] = {
    "nightly-sales": partial(
        ReportJob,
        name="nightly-sales",
        query="SELECT * FROM sales WHERE day = today()",
        recipients=("sales-leads@example.com",),
        filters=("exclude-test-accounts",),
    ),
    "weekly-audit": partial(
        ReportJob,
        name="weekly-audit",
        query="SELECT * FROM ledger WHERE week = this_week()",
        recipients=("finance@example.com", "cfo@example.com"),
        fmt="xlsx",
    ),
}


def schedule(template: str, **overrides: object) -> ReportJob:
    """A fresh, independently-owned job; overrides customize this run only."""
    job = TEMPLATES[template]()
    return replace(job, **overrides) if overrides else job  # type: ignore[arg-type]


@dataclass
class Scheduler:
    queue: list[ReportJob] = field(default_factory=list)

    def enqueue(self, template: str, **overrides: object) -> ReportJob:
        job = schedule(template, **overrides)
        self.queue.append(job)
        return job


def main() -> None:
    scheduler = Scheduler()
    scheduler.enqueue("nightly-sales")
    rush = scheduler.enqueue("weekly-audit", fmt="csv")
    print(f"queued: {[j.name for j in scheduler.queue]}")
    print(f"per-run override, template untouched: {rush.fmt} vs {schedule('weekly-audit').fmt}")


if __name__ == "__main__":
    main()
