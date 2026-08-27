"""Sandboxed execution of catalog example packages -- and nothing else.

The contract: only paths resolved from the catalog index are runnable.
The (id, example) pair is looked up, never joined into a path, so there is
no traversal and no arbitrary-file execution surface.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass

from design_patterns.catalog import Catalog

TIMEOUT_SECONDS = 10
MAX_OUTPUT_BYTES = 64 * 1024


@dataclass(frozen=True)
class RunResult:
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False


def _run_module(repo_root: str, module: str) -> RunResult:
    """Run ``python -I -m <module>`` with a scrubbed env, scratch cwd, and output caps."""
    # -I ignores PYTHONPATH by design, so the repo root (resolved by the
    # catalog, never by the caller) is injected in the bootstrap itself.
    bootstrap = (
        f"import sys, runpy; sys.path.insert(0, {repo_root!r}); "
        f"runpy.run_module({module!r}, run_name='__main__')"
    )
    with tempfile.TemporaryDirectory() as scratch_cwd:
        try:
            completed = subprocess.run(
                [sys.executable, "-I", "-c", bootstrap],
                cwd=scratch_cwd,
                env={},  # scrubbed environment
                capture_output=True,
                timeout=TIMEOUT_SECONDS,
                text=True,
            )
        except subprocess.TimeoutExpired as exc:
            out = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            err = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            return RunResult(
                exit_code=-1,
                stdout=out[:MAX_OUTPUT_BYTES],
                stderr=err[:MAX_OUTPUT_BYTES],
                timed_out=True,
            )
    return RunResult(
        exit_code=completed.returncode,
        stdout=completed.stdout[:MAX_OUTPUT_BYTES],
        stderr=completed.stderr[:MAX_OUTPUT_BYTES],
    )


def run_example_package(catalog: Catalog, pattern_id: str, example: str) -> RunResult:
    """Execute a unit's ``examples/<example>`` mini-project in a subprocess."""
    pattern = catalog.get(pattern_id)  # KeyError for unknown ids -- by design
    examples = pattern.examples()
    if example not in examples:
        raise KeyError(f"{pattern_id} has no example {example!r} (has: {sorted(examples)})")
    path = examples[example]  # resolved by the catalog, never by the caller
    if not (path / "main.py").is_file():  # a real check, not an assert: survives python -O
        raise FileNotFoundError(f"catalog names {path} but it has no main.py")

    repo_root = pattern.path.parents[2]
    module = f"patterns.{pattern.group}.{pattern.slug}.examples.{example}.main"
    return _run_module(str(repo_root), module)
