"""Domain types for the report-job mini-project."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReportJob:
    """One scheduled report run. Frozen: per-run tweaks build a new job."""

    name: str
    query: str
    recipients: tuple[str, ...]
    fmt: str = "pdf"
    filters: tuple[str, ...] = ()
