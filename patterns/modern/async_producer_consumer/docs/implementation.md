# Async Producer/Consumer — implementation guide

## The smell that calls for it

An `async` code path does `for item in items: await do(item)` and the wall
clock shows it — sequential awaits over independent I/O. Or the opposite:
`gather` over ten thousand tasks and memory shows *that*.

## Introducing it, step by step

1. **Isolate the per-item coroutine.** One `async def process(item) -> result`
   with no shared state. This is the seam everything else plugs into.
2. **Pick the memory budget.** `maxsize` is how many items may sit fetched-
   but-unprocessed. Small (2–16) is almost always right; it exists to create
   backpressure, not to be a cache.
3. **Pick the worker count.** Concurrency toward the slow resource — for
   HTTP this is "how many connections is polite", not "how many items exist".
4. **Pick the shutdown discipline — and write the test the same day.**
   - `Shutdown.JOIN_AND_CANCEL` when a coordinator knows the item set and
     wants "everything finished" as a joinable event.
   - `Shutdown.SENTINEL` when the producer itself signals the end of a
     stream and workers should drain and stop.
5. **Decide the failure policy at the edge.** The pool is fail-fast (one bad
   item cancels the run, surfacing as an `ExceptionGroup`). If a bad item
   must not kill the batch, catch inside *your* processor and return an
   outcome object — as the [feed_fetcher example](../examples/feed_fetcher/)
   does with `FetchOutcome`.

## Idioms

- `async with asyncio.TaskGroup()` owns the workers; nothing outlives the
  block, and worker exceptions propagate instead of vanishing.
- Results in completion order, ordering as the caller's last step — sorting
  inside the pool would hide the concurrency it exists to provide.
- The same shape works threaded (`queue.Queue`, `concurrent.futures`) when
  the work is blocking rather than async; the design choices carry over.

## Pitfalls

- **Unbounded queue.** `asyncio.Queue()` with no `maxsize` removes the
  backpressure that is half the pattern's point.
- **Mixed disciplines.** `task_done()` bookkeeping *and* sentinels in the
  same pool — each looks redundant, together they deadlock or exit early.
- **Sentinel miscounting.** Fewer end-markers than workers hangs the rest;
  route all shutdown through one tested code path (the pool), not call sites.
- **CPU-bound processors.** The event loop runs one coroutine at a time;
  workers give you interleaved I/O waits, never parallel computation.
