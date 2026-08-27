"""Demo: one settings object for the process, and the test-reset seam."""

from __future__ import annotations

import os

from patterns.creational.singleton.examples.app_config.settings import (
    get_settings,
    load_settings,
    reset_settings,
)


def main() -> None:
    first = get_settings()
    print(f"settings:          env={first.env} workers={first.max_workers}")
    print(f"same object twice: {get_settings() is first}")

    reset_settings()
    print(f"fresh after reset: {get_settings() is not first}")

    os.environ["APP_MAX_WORKERS"] = "16"
    try:
        print(f"still cached:      workers={get_settings().max_workers}")
        reset_settings()
        print(f"reset re-reads:    workers={get_settings().max_workers}")
    finally:
        del os.environ["APP_MAX_WORKERS"]
        reset_settings()

    canned = load_settings({"APP_ENV": "test", "APP_DEBUG": "1"})
    print(f"injected mapping:  env={canned.env} debug={canned.debug}")


if __name__ == "__main__":
    main()
