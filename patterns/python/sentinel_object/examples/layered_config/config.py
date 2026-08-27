"""Layered configuration where ``None`` is a value, not an absence.

Settings resolve CLI ← file ← defaults. A stored ``None`` means "explicitly
disabled" — a real decision someone made — so "missing" needs its own marker:
the sentinel, checked by identity.
"""

from __future__ import annotations

from collections.abc import Mapping

from patterns.python.sentinel_object.pattern import MISSING, Sentinel

Value = str | int | None


class LayeredConfig:
    """Lookup through override layers, None-safe at every step."""

    def __init__(
        self,
        defaults: Mapping[str, Value],
        file: Mapping[str, Value] | None = None,
        cli: Mapping[str, Value] | None = None,
    ) -> None:
        # Highest priority first.
        self._layers: tuple[tuple[str, Mapping[str, Value]], ...] = (
            ("cli", dict(cli or {})),
            ("file", dict(file or {})),
            ("defaults", dict(defaults)),
        )

    def get(self, key: str, default: Value | Sentinel = MISSING) -> Value:
        """The first layer that *has* the key wins — even when its value is None."""
        for _, layer in self._layers:
            value = layer.get(key, MISSING)
            if not isinstance(value, Sentinel):
                return value
        if isinstance(default, Sentinel):
            raise KeyError(f"{key!r} not set in any layer and no default given")
        return default

    def source_of(self, key: str) -> str:
        """Which layer answers for a key — 'unset' if none does."""
        for name, layer in self._layers:
            if key in layer:
                return name
        return "unset"
