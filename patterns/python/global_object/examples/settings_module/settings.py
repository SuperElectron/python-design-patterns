"""The application's shared globals, one of each legitimate kind.

Constants and a cheap prebuilt object are assigned at import time; the one
expensive resource hides behind ``Lazy`` so importing this module never does
more work than defining names. ``FACTORY_RUNS`` exists so tests can *prove*
that discipline instead of trusting it.
"""

from __future__ import annotations

import re

from patterns.python.global_object.pattern import Lazy

#: The Constant Pattern: immutable, named, computed once.
RETRY_LIMIT = 3
SUPPORTED_LOCALES = frozenset({"en", "fr", "de"})

#: A cheap, pure prebuilt object — a compiled regex is fine at import time.
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")

#: Counts factory runs; tests assert it stays 0 until first use, then 1.
FACTORY_RUNS = 0


def _build_zone_table() -> dict[str, int]:
    """Stand-in for the expensive load (file parse, DNS, warehouse query)."""
    global FACTORY_RUNS
    FACTORY_RUNS += 1
    zones = {"CA": 1, "US": 1, "MX": 2, "FR": 3, "DE": 3}
    return {country: zone for country, zone in sorted(zones.items())}


#: The expensive global: constructed on first ``ZONE_TABLE.get()``, never at import.
ZONE_TABLE: Lazy[dict[str, int]] = Lazy(_build_zone_table)
