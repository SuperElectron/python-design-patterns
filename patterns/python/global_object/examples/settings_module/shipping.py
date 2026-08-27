"""A consumer module: uses the shared globals, never rebuilds them."""

from __future__ import annotations

from patterns.python.global_object.examples.settings_module import settings


def is_valid_slug(candidate: str) -> bool:
    return settings.SLUG.fullmatch(candidate) is not None


def shipping_zone(country: str) -> int:
    """Zone lookup pays the table's construction cost on the first call only."""
    table = settings.ZONE_TABLE.get()
    try:
        return table[country]
    except KeyError:
        raise ValueError(f"no shipping zone for {country!r}") from None
