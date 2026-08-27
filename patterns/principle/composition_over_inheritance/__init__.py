"""Composition Over Inheritance — public API.

>>> from patterns.principle.composition_over_inheritance import Filter, Logger
"""

from patterns.principle.composition_over_inheritance.pattern import (
    Filter,
    Logger,
    Sink,
    Transform,
    identity,
)

__all__ = ["Filter", "Logger", "Sink", "Transform", "identity"]
