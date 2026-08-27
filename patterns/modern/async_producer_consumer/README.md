---
id: modern/async_producer_consumer
name: Async Producer/Consumer
aliases: [asyncio-queue, worker-pool, pipeline]
guide_url: null
problem: "Decouple work generation from work processing under asyncio, with bounded memory and clean shutdown."
symptoms: ["fan out downloads to workers", "bounded queue backpressure", "asyncio pipeline", "graceful worker shutdown"]
verdict: use-with-care
caveats:
  - "Choose one shutdown discipline and test it: sentinels per worker, or queue.join() plus task cancellation."
  - "An unbounded queue turns a slow consumer into a memory leak — set maxsize and let backpressure work."
stdlib_sightings: [asyncio.Queue, asyncio.TaskGroup, queue.Queue]
---

# Async Producer/Consumer

Fan I/O-bound work out to N workers over a bounded queue — backpressure by
`maxsize`, shutdown as an explicit, tested choice. **Verdict: use with care**
— the right tool for async fan-out; the two caveats are where it bites.

| Where | What |
|---|---|
| [`pattern/`](pattern/) | The importable code: `WorkerPool`, `Shutdown`, `process_all` |
| [`docs/`](docs/) | [Fundamentals](docs/fundamentals.md) · [Implementation guide](docs/implementation.md) · [External examples](docs/examples.md) |
| [`examples/feed_fetcher/`](examples/feed_fetcher/) | Mini-project: feed pipeline with per-item failure capture, both shutdown disciplines |
| [`tests/`](tests/) | Behavioral tests for the pool and the mini-project |

```bash
uv run python -m patterns.modern.async_producer_consumer.examples.feed_fetcher.main
```
