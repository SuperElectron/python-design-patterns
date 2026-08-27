"""App configuration behind an accessor, built on the Singleton's replacement.

Run it: ``uv run python -m patterns.creational.singleton.examples.app_config``
"""

from patterns.creational.singleton.examples.app_config.settings import (
    Settings,
    get_settings,
    load_settings,
    reset_settings,
)

__all__ = ["Settings", "get_settings", "load_settings", "reset_settings"]
