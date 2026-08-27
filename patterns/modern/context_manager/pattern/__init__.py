"""The context manager pattern, importable as library code."""

from patterns.modern.context_manager.pattern.managers import AtomicWrite, temporarily

__all__ = ["AtomicWrite", "temporarily"]
