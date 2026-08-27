"""Stacking the decorators into a hardened charge function.

The stack reads bottom-up: retry hugs the flaky call so each attempt is
retried; logging sits outside so one *successful* operation logs once, not
once per attempt; the rate limit is outermost so rejected calls never touch
the network at all. That ordering is policy, and the tests pin it.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from patterns.structural.decorator.examples.resilient_client.client import (
    FlakyPaymentAPI,
    TransientNetworkError,
)
from patterns.structural.decorator.pattern import logged, rate_limited, retry


def build_charge(
    api: FlakyPaymentAPI,
    *,
    log: Callable[[str], None],
    max_attempts: int = 3,
    max_calls: int = 5,
    window: float = 1.0,
    clock: Callable[[], float] = time.monotonic,
) -> Callable[[str, int], str]:
    """Wrap ``api.charge`` in retry -> logging -> rate limit, innermost first."""

    def charge(card: str, amount_cents: int) -> str:
        """Charge a card once."""
        return api.charge(card, amount_cents)

    hardened = retry(max_attempts, on=(TransientNetworkError,))(charge)
    hardened = logged(log)(hardened)
    return rate_limited(max_calls, window, clock)(hardened)
