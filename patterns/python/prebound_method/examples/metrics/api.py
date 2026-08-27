"""The pattern applied: a ``random``-style module API over shared state.

One hidden collector is built at import time (cheap: two empty dicts); its
bound methods become the module's public functions. Callers write
``metrics.increment("orders")`` — no instance in sight — while the instance
rides along inside each bound method.
"""

from __future__ import annotations

from patterns.python.prebound_method.examples.metrics.collector import MetricsCollector

_collector = MetricsCollector()

#: The pattern: module-level names bound to the hidden instance's methods.
increment = _collector.increment
timing = _collector.timing
snapshot = _collector.snapshot
reset = _collector.reset
