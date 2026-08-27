"""Strategy — public API.

>>> from patterns.behavioral.strategy import StrategyRegistry
"""

from patterns.behavioral.strategy.pattern import StrategyRegistry, UnknownStrategyError

__all__ = ["StrategyRegistry", "UnknownStrategyError"]
