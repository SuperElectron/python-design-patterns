# Observer — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing event/notification code.

## Python standard library

- **`concurrent.futures.Future.add_done_callback`.** Register any callable
  on a future; it fires on completion — and fires *immediately* if the
  future already resolved, a late-subscriber decision worth copying.
  [docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.add_done_callback](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.add_done_callback)
- **`asyncio` callbacks.** The event loop's core currency:
  `loop.call_soon`, future/task done-callbacks — completion observers
  driving the whole async machine.
  [docs.python.org/3/library/asyncio-eventloop.html](https://docs.python.org/3/library/asyncio-eventloop.html) ·
  [docs.python.org/3/library/asyncio-future.html](https://docs.python.org/3/library/asyncio-future.html)

## Major ecosystems

- **Django signals.** `post_save`, `request_finished`, custom signals — the
  canonical Python pub/sub, with `@receiver` as decorator subscription. Its
  docs' warning that signals make flow "harder to follow" is the pattern's
  main cost, stated by its biggest user.
  [docs.djangoproject.com/en/stable/topics/signals/](https://docs.djangoproject.com/en/stable/topics/signals/)
- **blinker** — the standalone signals library Flask builds on; named
  signals, weak references to subscribers (an answer to the lapsed-listener
  leak). [blinker.readthedocs.io](https://blinker.readthedocs.io/) *(unverified)*
- **traitlets** — observable attributes (`observe`/`@observe`) powering
  Jupyter's configuration system; the property-setter idiom grown into a
  framework. [traitlets.readthedocs.io](https://traitlets.readthedocs.io/) *(unverified)*

## Outside Python, for contrast

- **DOM `addEventListener`** — the same shape every web developer already
  knows: subscribe callables to a subject's named events; `removeEventListener`
  is the lapsed-listener chore made visible.

## What to notice across all of them

Each one had to answer the two questions the classic diagram skips: *what
order* (Django: registration order; DOM: registration order per phase) and
*what happens when a listener throws* (Django propagates unless you use
`send_robust`; the DOM isolates). This module's `Signal` makes exactly those
two decisions explicit parameters.
