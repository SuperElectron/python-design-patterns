"""The async producer/consumer pattern, importable as library code."""

from patterns.modern.async_producer_consumer.pattern.pool import (
    Processor,
    Shutdown,
    WorkerPool,
    process_all,
)

__all__ = ["Processor", "Shutdown", "WorkerPool", "process_all"]
