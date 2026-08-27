"""A feature-flag rules engine built on the Interpreter pattern.

Run it: ``uv run python -m patterns.behavioral.interpreter.examples.flag_rules``
"""

from patterns.behavioral.interpreter.examples.flag_rules.engine import (
    OPERATIONS,
    FlagEngine,
)

__all__ = ["OPERATIONS", "FlagEngine"]
