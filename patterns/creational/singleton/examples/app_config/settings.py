"""Application settings built once, shared everywhere, resettable in tests.

The exact job Singleton is always reached for — one configuration object for
the whole process — done the Python way: a frozen ``Settings`` dataclass, a
loader that reads an environment *mapping* (injected, so tests never touch
the real ``os.environ``), and one ``Shared`` accessor giving lazy build,
process-wide sharing, and a reset seam. No ``__new__``, nothing hidden.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from patterns.creational.singleton.pattern import Shared


@dataclass(frozen=True)
class Settings:
    """Everything the app needs to know about its environment."""

    env: str
    database_url: str
    debug: bool
    max_workers: int


def load_settings(source: Mapping[str, str] | None = None) -> Settings:
    """Parse settings from an env-style mapping (``os.environ`` by default)."""
    env = os.environ if source is None else source
    return Settings(
        env=env.get("APP_ENV", "dev"),
        database_url=env.get("APP_DATABASE_URL", "sqlite:///dev.db"),
        debug=env.get("APP_DEBUG", "0") == "1",
        max_workers=int(env.get("APP_MAX_WORKERS", "4")),
    )


#: The one process-wide slot. Nothing is read until the first get_settings().
_shared: Shared[Settings] = Shared(load_settings)


def get_settings() -> Settings:
    """The app-wide accessor: same ``Settings`` object on every call."""
    return _shared.get()


def reset_settings() -> None:
    """Test seam: drop the cached instance so the next call re-reads the env."""
    _shared.reset()
