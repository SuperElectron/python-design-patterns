"""Behavioral tests for the resilient_client mini-project."""

from __future__ import annotations

import pytest

from patterns.structural.decorator.examples.resilient_client.client import FlakyPaymentAPI
from patterns.structural.decorator.examples.resilient_client.service import build_charge
from patterns.structural.decorator.pattern import RateLimitExceededError


def test_transient_failures_are_retried_away() -> None:
    api = FlakyPaymentAPI(failures=2)
    charge = build_charge(api, log=lambda _: None)
    assert charge("4242", 1200) == "txn-1"
    assert api.attempts == 3  # two failures + the success
    assert api.charges == [("4242", 1200)]


def test_stacking_order_logs_once_per_operation_not_per_attempt() -> None:
    lines: list[str] = []
    api = FlakyPaymentAPI(failures=2)
    charge = build_charge(api, log=lines.append)
    charge("4242", 500)
    # logged() sits OUTSIDE retry(): one arrow pair per operation, though the
    # network was hit three times. Swapping the layers would fail this test.
    assert lines == ["-> charge", "<- charge"]
    assert api.attempts == 3


def test_failures_beyond_the_retry_budget_surface() -> None:
    api = FlakyPaymentAPI(failures=5)
    charge = build_charge(api, log=lambda _: None, max_attempts=3)
    with pytest.raises(ConnectionError):
        charge("4242", 500)
    assert api.charges == []


def test_rate_limit_rejects_before_touching_the_network() -> None:
    now = [0.0]
    api = FlakyPaymentAPI(failures=0)
    charge = build_charge(api, log=lambda _: None, max_calls=2, window=60.0, clock=lambda: now[0])
    charge("4242", 100)
    charge("4242", 200)
    with pytest.raises(RateLimitExceededError):
        charge("4242", 300)
    assert api.attempts == 2  # the rejected call never reached the API


def test_hardened_callable_keeps_identity() -> None:
    charge = build_charge(FlakyPaymentAPI(failures=0), log=lambda _: None)
    assert charge.__name__ == "charge"
