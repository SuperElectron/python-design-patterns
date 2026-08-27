"""Demo: None-vs-missing through three config layers."""

from __future__ import annotations

from patterns.python.sentinel_object.examples.layered_config.config import LayeredConfig
from patterns.python.sentinel_object.examples.layered_config.notifier import notifier_for


def main() -> None:
    config = LayeredConfig(
        defaults={"timeout_s": 30, "alert_email": "ops@example.com", "proxy": None},
        file={"timeout_s": 60, "alert_email": None},  # None: someone turned alerts OFF
        cli={"timeout_s": 10},
    )
    for key in ("timeout_s", "alert_email", "proxy"):
        print(f"{key:12} = {config.get(key)!r:22} (from {config.source_of(key)})")
    notifier = notifier_for(config)
    notifier.notify("disk almost full")
    print(f"notifier     = {type(notifier).__name__} (file layer's None disabled alerts)")


if __name__ == "__main__":
    main()
