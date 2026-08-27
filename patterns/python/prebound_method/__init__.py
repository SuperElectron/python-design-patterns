"""Prebound Method — public API.

>>> from patterns.python.prebound_method import increment, peek
"""

from patterns.python.prebound_method.pattern import (
    Counter,
    increment,
    peek,
    shares_instance,
)

__all__ = ["Counter", "increment", "peek", "shares_instance"]
