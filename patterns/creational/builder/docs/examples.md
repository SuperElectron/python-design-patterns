# Builder — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing staged-construction code.

## Python standard library

- **`email.message.EmailMessage`.** Assembled call by call — headers by item
  assignment, body by `set_content` — and only serialized at the end: the
  builder-as-convenience in the stdlib.
  [docs.python.org/3/library/email.message.html](https://docs.python.org/3/library/email.message.html)
- **`configparser.ConfigParser`.** Accumulates sections and values through a
  mutable surface, then writes the finished representation out.
  [docs.python.org/3/library/configparser.html](https://docs.python.org/3/library/configparser.html)

## Major ecosystems

- **SQLAlchemy `select()`.** `select(...).where(...).order_by(...)` is a
  *generative* builder: each step returns a new immutable statement rather
  than mutating one — the same product-immutability discipline, taken one
  step further. [docs.sqlalchemy.org/en/20/core/selectable.html](https://docs.sqlalchemy.org/en/20/core/selectable.html)
- **Django `QuerySet` chaining.** `.filter(...).exclude(...).order_by(...)`
  refines an immutable, lazily-executed query per call.
  [docs.djangoproject.com/en/5.0/ref/models/querysets/](https://docs.djangoproject.com/en/5.0/ref/models/querysets/)
- **matplotlib `pyplot`.** The guide's headline example: a figure assembled
  through many convenience calls against implicit current state.
  [python-patterns.guide/gang-of-four/builder/](https://python-patterns.guide/gang-of-four/builder/)

## The guide chapter

python-patterns.guide's treatment — why keyword arguments dissolve the
telescoping constructor, and which builder survives:
[python-patterns.guide/gang-of-four/builder/](https://python-patterns.guide/gang-of-four/builder/)

## What to notice across all of them

None ship a Director, and none expose a mutable product: the stdlib builders
mutate *themselves* then emit/serialize, while SQLAlchemy and Django make even
the builder immutable (each step a new value). When reviewing a builder, ask
where the mutable/immutable line sits — and whether plain keyword arguments
would erase the class entirely.
