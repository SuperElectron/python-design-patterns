# Async Producer/Consumer — external examples

Real embodiments of the pattern outside this repo, for deeper study.

## Standard library

- **`asyncio.Queue`** — the buffer itself; the docs include a worked
  producer/consumer example that is this pattern verbatim.
  <https://docs.python.org/3/library/asyncio-queue.html>
- **`asyncio.TaskGroup`** (3.11+) — structured lifetime for the worker
  tasks; the reason the pool needs no manual join/cancel bookkeeping
  beyond its shutdown discipline.
  <https://docs.python.org/3/library/asyncio-task.html#task-groups>
- **`queue.Queue`** — the threaded flavor, with the same
  `task_done()`/`join()` contract the JOIN_AND_CANCEL discipline uses.
  <https://docs.python.org/3/library/queue.html>
- **`concurrent.futures`** — the pool-shaped alternative when items are
  independent and you want futures rather than a shared queue.
  <https://docs.python.org/3/library/concurrent.futures.html>

## Elsewhere

- **aiohttp** client examples — crawler-style fan-out over a session is
  this pattern with real HTTP in the processor seam. *(unverified)*
  <https://docs.aiohttp.org/>
