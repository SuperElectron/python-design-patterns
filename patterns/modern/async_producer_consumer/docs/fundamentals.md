# Async Producer/Consumer — fundamentals

## Intent

Decouple work *generation* from work *processing*: producers enqueue, N
consumers dequeue and process, and a bounded buffer between them keeps a fast
side from drowning a slow one. Under asyncio the pattern is how you fan
I/O-bound work out to concurrent workers with bounded memory and a shutdown
that neither drops items nor hangs.

## Participants

| Role | Classic (threaded) form | asyncio form |
|---|---|---|
| Buffer | `queue.Queue` + locks/conditions | `asyncio.Queue(maxsize=...)` — backpressure built in |
| Producers | Threads calling `put` | Any coroutine calling `await queue.put(item)` |
| Consumers | Worker threads in a `get` loop | N worker tasks — `WorkerPool` in [`pattern/pool.py`](../pattern/pool.py) |
| Worker lifetime | Manual `start`/`join` | `asyncio.TaskGroup` owns the tasks structurally |
| Shutdown discipline | Ad hoc, often forgotten | An explicit choice: `Shutdown.SENTINEL` or `Shutdown.JOIN_AND_CANCEL` |

## Mechanism

1. A bounded queue is created; `maxsize` is the memory budget *and* the
   backpressure valve — `put` blocks when the buffer is full.
2. N workers start, each looping `get → process`.
3. Producers enqueue items; slow consumers automatically slow the producers.
4. Shutdown, the part naive versions get wrong, is one of two disciplines:
   - **Sentinel** — after the last item, enqueue one end-marker per worker;
     each worker exits on dequeuing one.
   - **Join and cancel** — workers mark `task_done()`; the coordinator awaits
     `queue.join()` (every item fetched *and* finished), then cancels the
     now-idle workers.

## The classic form, and what Python absorbs

Before asyncio this was the thread pattern — an OS thread per worker, a lock
around shared results, and hand-rolled sentinel plumbing:

```python
def process_all(items: list[str], worker_count: int = 2) -> list[str]:
    channel: queue.Queue[str | None] = queue.Queue()
    results: list[str] = []
    lock = threading.Lock()

    def worker() -> None:
        while (item := channel.get()) is not None:
            with lock:
                results.append(item.upper())

    workers = [threading.Thread(target=worker) for _ in range(worker_count)]
    for w in workers:
        w.start()
    for item in items:
        channel.put(item)
    for _ in workers:
        channel.put(None)  # one sentinel per worker — forget one and it hangs
    for w in workers:
        w.join()
    return sorted(results)
```

`asyncio.Queue` absorbs the locking entirely and `TaskGroup` absorbs the
lifetime bookkeeping. What Python does *not* absorb is the design: choosing
`maxsize`, and choosing — then testing — the shutdown discipline. That
remainder is the pattern.

## When to use it

- Many I/O-bound items (fetches, uploads, API calls) and you want bounded
  concurrency rather than a task per item.
- Producers and consumers run at different, varying speeds and you need
  memory to stay bounded in between.

## When not to use it

- CPU-bound work — an event loop serializes it; use a process pool.
- Independent items with no need to bound in-flight memory —
  `asyncio.gather` (or `TaskGroup` alone) over per-item tasks is simpler.
- One item, one consumer — that is just an awaited call.

## Verdict: use with care

The right tool for I/O fan-out, with two sharp edges the caveats name: an
unbounded queue turns a slow consumer into a memory leak, and an untested
shutdown path is where these systems hang. `WorkerPool` makes both choices
explicit arguments so they cannot be forgotten — only wrong on purpose.
