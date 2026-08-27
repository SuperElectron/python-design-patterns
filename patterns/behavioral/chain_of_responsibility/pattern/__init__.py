"""The Chain of Responsibility pattern, importable as library code."""

from patterns.behavioral.chain_of_responsibility.pattern.chain import (
    Chain,
    Handler,
    UnhandledRequestError,
)

__all__ = ["Chain", "Handler", "UnhandledRequestError"]
