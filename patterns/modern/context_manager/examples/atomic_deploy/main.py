"""Demo: a good release deploys; a bad one rolls back completely."""

from __future__ import annotations

import tempfile
from pathlib import Path

from patterns.modern.context_manager.examples.atomic_deploy.deploy import (
    ReleaseError,
    deploy,
    require_nonempty,
)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        deploy({"app.toml": "retries = 3\n", "logging.toml": "level = 'info'\n"}, target)
        print(f"v1 deployed: {sorted(p.name for p in target.iterdir())}")

        bad_release = {"app.toml": "retries = 5\n", "logging.toml": "   "}
        try:
            deploy(bad_release, target, validate=require_nonempty)
        except ReleaseError as exc:
            print(f"v2 rejected ({exc})")
        print(f"app.toml still reads: {(target / 'app.toml').read_text().strip()}")


if __name__ == "__main__":
    main()
