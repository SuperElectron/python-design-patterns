"""The Proxy pattern, importable as library code."""

from patterns.structural.proxy.pattern.proxies import (
    LazyProxy,
    MeteringProxy,
    ProtectionProxy,
)

__all__ = ["LazyProxy", "MeteringProxy", "ProtectionProxy"]
