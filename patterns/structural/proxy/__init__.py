"""Proxy — public API.

>>> from patterns.structural.proxy import LazyProxy
"""

from patterns.structural.proxy.pattern import (
    LazyProxy,
    MeteringProxy,
    ProtectionProxy,
)

__all__ = ["LazyProxy", "MeteringProxy", "ProtectionProxy"]
