# Mediator — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing coordinator-shaped code.

## Python standard library

- **`queue.Queue` / `asyncio.Queue`** — the degenerate mediator: producers
  and consumers know the queue and never each other; the pairwise coupling
  that would exist lives in one thread-safe object.
  [docs.python.org/3/library/queue.html](https://docs.python.org/3/library/queue.html)
- **Tk variable tracing** — `tkinter` widgets coordinate through shared
  `Variable` objects with trace callbacks rather than direct references.
  [docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html) *(unverified)*

## Major ecosystems

- **Django `Form.clean()`** — cross-field validation in one method: fields
  that depend on each other never reference each other; the form owns the
  rule ("if shipping is express, phone is required").
  [docs.djangoproject.com/en/stable/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other](https://docs.djangoproject.com/en/stable/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other)
- **python-telegram-bot's `Application`** — handlers register with one
  dispatcher; updates route through it; handlers never call each other.
  [docs.python-telegram-bot.org](https://docs.python-telegram-bot.org/) *(unverified)*
- **Message brokers (RabbitMQ, Kafka)** — the mediator at architecture
  scale: every producer and consumer couples to the broker's topology, none
  to each other. The god-object risk scales up too — topic sprawl is
  `recheck` sprawl. *(concept citation)*

## What to notice across all of them

Each one is defined by the references it *removes* — Django fields don't
import each other, queue consumers can't name their producers. And each
bounds the mediator's scope: `clean()` owns validation only, a queue owns
transport only. When reviewing mediator code, ask what pairwise references
died, and what stops the hub from absorbing rules that belong to the domain.
