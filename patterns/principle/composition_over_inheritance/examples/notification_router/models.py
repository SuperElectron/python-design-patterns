"""Domain types for the notification-router mini-project."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Alert:
    """Something worth telling someone about. Severity: 1 (info) .. 5 (page)."""

    source: str
    severity: int
    message: str
