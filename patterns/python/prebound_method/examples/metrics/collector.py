"""The public class behind the metrics module's friendly face.

Stays public on purpose: libraries and tests build their own isolated
collector, exactly as ``random.Random`` stays public beside ``random.random``.
"""

from __future__ import annotations


class MetricsCollector:
    """Counts and timings for one scope (the process, or one test)."""

    def __init__(self) -> None:
        self._counts: dict[str, int] = {}
        self._timings: dict[str, list[float]] = {}

    def increment(self, name: str, by: int = 1) -> int:
        """Bump a counter; returns its new value."""
        self._counts[name] = self._counts.get(name, 0) + by
        return self._counts[name]

    def timing(self, name: str, milliseconds: float) -> None:
        """Record one duration observation."""
        self._timings.setdefault(name, []).append(milliseconds)

    def snapshot(self) -> dict[str, object]:
        """An immutable-ish view: counters plus per-name timing averages."""
        averages = {
            name: sum(values) / len(values) for name, values in self._timings.items() if values
        }
        return {"counts": dict(self._counts), "timing_avg_ms": averages}

    def reset(self) -> None:
        """Forget everything — the seam tests use between cases."""
        self._counts.clear()
        self._timings.clear()
