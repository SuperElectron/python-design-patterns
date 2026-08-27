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

## Problem

Producers generate work faster (or slower) than consumers process it. You
want N workers pulling from a shared source, bounded memory in between, and
a shutdown that neither drops items nor hangs.

## Naive solution

`naive.py` is the thread version: `threading.Thread` workers around a
`queue.Queue` with sentinels — fine, but each worker burns an OS thread and
coordination is manual.

## Pythonic solution

`asyncio.Queue` with `TaskGroup`-managed workers: `maxsize` gives
backpressure, `queue.join()` waits for completion, cancellation ends the
idle workers. All the coordination is in the queue.

## In the wild

This *is* the stdlib idiom — the asyncio docs' own queue example is this
pattern; `real_world.py` shapes it as a rate-limited fetch pipeline with
per-item results collected in completion order.

## Verdict

**Use with care.** The right tool for I/O-bound fan-out; get the shutdown
discipline right (and tested) or debug it forever.
