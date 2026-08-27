"""Visitor — public API.

>>> from patterns.behavioral.visitor import Operation
"""

from patterns.behavioral.visitor.pattern import Operation, UnhandledNodeError

__all__ = ["Operation", "UnhandledNodeError"]
