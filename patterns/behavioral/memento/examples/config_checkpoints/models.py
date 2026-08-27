"""Domain types for the config-checkpoints mini-project."""

from __future__ import annotations

from dataclasses import dataclass

LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR"})


class InvalidConfigError(ValueError):
    """The proposed configuration violates at least one rule."""


@dataclass(frozen=True)
class ServiceConfig:
    """A service's settings. Frozen: every edit produces a new snapshot."""

    workers: int = 2
    timeout_s: float = 30.0
    log_level: str = "INFO"
    feature_flags: frozenset[str] = frozenset()


def validate(config: ServiceConfig) -> None:
    """Raise ``InvalidConfigError`` naming every rule the config breaks."""
    problems: list[str] = []
    if config.workers < 1:
        problems.append(f"workers must be >= 1, got {config.workers}")
    if config.timeout_s <= 0:
        problems.append(f"timeout_s must be positive, got {config.timeout_s}")
    if config.log_level not in LOG_LEVELS:
        problems.append(f"log_level must be one of {sorted(LOG_LEVELS)}, got {config.log_level!r}")
    if problems:
        raise InvalidConfigError("; ".join(problems))
