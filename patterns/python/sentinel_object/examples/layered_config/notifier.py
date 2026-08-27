"""The neighboring Null Object cure, in the same domain.

``alert_email = None`` means notifications are explicitly disabled. Instead
of every caller branching on that, ``notifier_for`` hands back a NullNotifier
— a real object that intentionally does nothing — and callers stop checking.
"""

from __future__ import annotations

from patterns.python.sentinel_object.examples.layered_config.config import LayeredConfig


class EmailNotifier:
    """Fake outbound email; records sends so behavior is testable."""

    def __init__(self, address: str) -> None:
        self.address = address
        self.sent: list[str] = []

    def notify(self, message: str) -> None:
        self.sent.append(f"to {self.address}: {message}")


class NullNotifier:
    """The Null Object: same interface, deliberate no-op, no None checks."""

    def notify(self, message: str) -> None:
        pass


def notifier_for(config: LayeredConfig) -> EmailNotifier | NullNotifier:
    """None (explicitly disabled) and unset both mean: the silent notifier."""
    address = config.get("alert_email", default=None)
    if isinstance(address, str):
        return EmailNotifier(address)
    return NullNotifier()
