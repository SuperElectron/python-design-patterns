# Composition Over Inheritance — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing class hierarchies.

## Python standard library

- **`logging`.** The guide's own worked example, shipped at scale: `Logger`
  composes `Handler`s, `Filter`s, and `Formatter`s — four orthogonal axes,
  no class per combination.
  [docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html)
- **`socketserver`.** The honest contrast: the stdlib's mixin dodge
  (`ThreadingMixIn` + `TCPServer` = `ThreadingTCPServer`), useful to study
  as the alternative the principle warns will reconverge on the diamond.
  [docs.python.org/3/library/socketserver.html](https://docs.python.org/3/library/socketserver.html)

## Major ecosystems

- **pytest's plugin architecture.** Behavior is added by composing plugins
  registered with hook functions — not by subclassing the test runner.
  [docs.pytest.org/en/stable/how-to/writing_plugins.html](https://docs.pytest.org/en/stable/how-to/writing_plugins.html)
- **The guide chapter** — the subclass-explosion case study and the taxonomy
  of dodges (multiple inheritance, mixins, dynamically built classes).
  [python-patterns.guide/gang-of-four/composition-over-inheritance](https://python-patterns.guide/gang-of-four/composition-over-inheritance/)

## What to notice across all of them

In every healthy example the *combination* is expressed at runtime — a
constructor call, a registration — while the *pieces* stay single-purpose.
When reviewing, count adjectives in class names: two or more is the explosion
starting.
