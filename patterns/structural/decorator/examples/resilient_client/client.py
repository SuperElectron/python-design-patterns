"""The unreliable thing being hardened: a fake payments API."""

from __future__ import annotations

from dataclasses import dataclass, field


class TransientNetworkError(ConnectionError):
    """The kind of failure a retry can reasonably paper over."""


@dataclass
class FlakyPaymentAPI:
    """Fails the first ``failures`` calls, then succeeds forever after."""

    failures: int
    attempts: int = 0
    charges: list[tuple[str, int]] = field(default_factory=list)

    def charge(self, card: str, amount_cents: int) -> str:
        self.attempts += 1
        if self.attempts <= self.failures:
            raise TransientNetworkError(f"connection reset (attempt {self.attempts})")
        self.charges.append((card, amount_cents))
        return f"txn-{len(self.charges)}"
