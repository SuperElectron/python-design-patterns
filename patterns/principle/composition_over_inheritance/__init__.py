"""Composition Over Inheritance — public API.

>>> from patterns.principle.composition_over_inheritance import Pipeline, Logger
"""

from patterns.principle.composition_over_inheritance.pattern import (
    Filter,
    Logger,
    Pipeline,
    Sink,
    Transform,
    identity,
)

__all__ = ["Filter", "Logger", "Pipeline", "Sink", "Transform", "identity"]
