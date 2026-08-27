"""The Visitor pattern, importable as library code."""

from patterns.behavioral.visitor.pattern.dispatch import Operation, UnhandledNodeError

__all__ = ["Operation", "UnhandledNodeError"]
