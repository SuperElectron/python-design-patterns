"""Async Producer/Consumer — public API.

>>> from patterns.modern.async_producer_consumer import WorkerPool
"""

from patterns.modern.async_producer_consumer.pattern import (
    Processor,
    Shutdown,
    WorkerPool,
    process_all,
)

__all__ = ["Processor", "Shutdown", "WorkerPool", "process_all"]
