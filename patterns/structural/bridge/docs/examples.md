# Bridge — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing bridge-shaped code.

## Python standard library

- **`logging.Logger` × `logging.Handler`.** The logger is the abstraction
  callers hold; handlers are the interchangeable implementation hierarchy —
  one `logger.info()` call fans out to console, file, or syslog backends, and
  both sides grow independently.
  [docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html)

## Major ecosystems

- **Matplotlib figures over rendering backends.** The `Figure`/`Artist`
  layer is one stable abstraction; Agg, SVG, PDF, and GUI canvases are
  swappable implementors selected at runtime — the canonical large-scale
  bridge.
  [matplotlib.org/stable/users/explain/figure/backends.html](https://matplotlib.org/stable/users/explain/figure/backends.html)
- **Django ORM over database backends.** One `QuerySet` abstraction compiles
  through per-database implementor packages (PostgreSQL, MySQL, SQLite…);
  application code never learns which.
  [docs.djangoproject.com/en/stable/ref/databases/](https://docs.djangoproject.com/en/stable/ref/databases/)
- **SQLAlchemy `Engine` over `Dialect`/DBAPI.** The same split one level
  down: Core's execution abstraction bridges to per-driver dialects.
  [docs.sqlalchemy.org/en/20/core/engines.html](https://docs.sqlalchemy.org/en/20/core/engines.html)

## What to notice across all of them

The implementor interface is always *narrow and stable* — `Handler.emit`,
the backend canvas API, the dialect contract — while both sides multiply
freely behind it. When reviewing bridge-shaped code, check which axis a new
requirement lands on: if most changes touch both sides at once, the axes were
drawn in the wrong place.
