"""The Strategy pattern, importable as library code."""

from patterns.behavioral.strategy.pattern.registry import (
    StrategyRegistry,
    UnknownStrategyError,
)

__all__ = ["StrategyRegistry", "UnknownStrategyError"]
