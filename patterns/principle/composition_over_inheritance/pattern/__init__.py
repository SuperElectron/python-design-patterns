"""Composition Over Inheritance, importable as library code."""

from patterns.principle.composition_over_inheritance.pattern.compose import (
    Filter,
    Logger,
    Pipeline,
    Sink,
    Transform,
    identity,
)

__all__ = ["Filter", "Logger", "Pipeline", "Sink", "Transform", "identity"]
