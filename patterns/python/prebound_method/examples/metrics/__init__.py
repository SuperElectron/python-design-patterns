"""Process-wide metrics built on the Prebound Method pattern.

Run it: ``uv run python -m patterns.python.prebound_method.examples.metrics``
"""

from patterns.python.prebound_method.examples.metrics.api import (
    increment,
    reset,
    snapshot,
    timing,
)
from patterns.python.prebound_method.examples.metrics.collector import MetricsCollector

__all__ = ["MetricsCollector", "increment", "reset", "snapshot", "timing"]
