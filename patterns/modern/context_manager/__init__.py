"""Context Manager — public API.

>>> from patterns.modern.context_manager import AtomicWrite
"""

from patterns.modern.context_manager.pattern import AtomicWrite, temporarily

__all__ = ["AtomicWrite", "temporarily"]
