"""A small app's settings module done right, built on the Global Object pattern.

Run it: ``uv run python -m patterns.python.global_object.examples.settings_module``
"""

from patterns.python.global_object.examples.settings_module.settings import (
    RETRY_LIMIT,
    SLUG,
    SUPPORTED_LOCALES,
    ZONE_TABLE,
)
from patterns.python.global_object.examples.settings_module.shipping import (
    is_valid_slug,
    shipping_zone,
)

__all__ = [
    "RETRY_LIMIT",
    "SLUG",
    "SUPPORTED_LOCALES",
    "ZONE_TABLE",
    "is_valid_slug",
    "shipping_zone",
]
