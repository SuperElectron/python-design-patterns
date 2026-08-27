---
id: creational/builder
name: Builder
aliases: [fluent-builder]
guide_url: https://python-patterns.guide/gang-of-four/builder/
problem: "Assemble a complex object step by step, so the assembly process is reusable and readable."
symptoms: ["constructor with ten arguments", "object needs staged assembly", "fluent chained construction", "same steps, different representations"]
verdict: use-with-care
caveats:
  - "Python's keyword arguments with defaults already solve the 'telescoping constructor' problem the GoF Builder exists for."
  - "The guide's verdict: the Builder survives in Python mainly as a convenience for callers (e.g. matplotlib's pyplot), not as a construction ceremony."
stdlib_sightings: [email.message.EmailMessage, configparser.ConfigParser]
---

# Builder

## Problem

Some objects are miserable to construct in one shot: many parts, ordering
constraints, optional pieces. In 1994 Java/C++ the answer was a separate
Builder class walked by a Director, so the same step sequence could produce
different representations.

## Naive solution

`naive.py` is the full ceremony: an abstract builder interface, two concrete
builders, and a director that walks the steps. Faithful to the book — and
visibly over-engineered for Python.

## Pythonic solution

Python removes the two problems the pattern solved. Keyword arguments with
defaults kill the telescoping constructor, and first-class classes mean "the
same process, different representation" is just passing a different callable.
What *survives* is the Builder-as-convenience: a friendly object that
accumulates settings and then emits the real, immutable product —
`pythonic.py` builds a frozen dataclass through one.

## In the wild

`email.message.EmailMessage` is a builder you mutate call by call
(`msg["To"] = ...`, `set_content(...)`) before serializing;
`configparser.ConfigParser` accumulates sections the same way. Matplotlib's
`pyplot` interface is the guide's own headline example.

## Verdict

**Use with care.** Reach for keyword arguments first. Write a builder when
construction is genuinely staged or when you want a mutable assembly surface
in front of an immutable product.
