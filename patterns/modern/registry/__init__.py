"""Registry — public API.

>>> from patterns.modern.registry import Registry
"""

from patterns.modern.registry.pattern import Registry, UnknownKeyError

__all__ = ["Registry", "UnknownKeyError"]
