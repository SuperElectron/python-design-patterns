# Iterator — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing traversal code.

## Python standard library

- **Generators and `itertools`** — the pattern as language feature plus a
  toolbox of composable iterators (`count`, `islice`, `chain`, `tee`).
  [docs.python.org/3/library/itertools.html](https://docs.python.org/3/library/itertools.html)
- **`os.walk` / `pathlib.Path.iterdir`** — lazy filesystem traversal: a
  directory tree of any size, constant memory.
  [docs.python.org/3/library/os.html#os.walk](https://docs.python.org/3/library/os.html#os.walk)
- **`csv.reader`** — file rows as an iterator; the file object underneath is
  itself an iterator of lines.
  [docs.python.org/3/library/csv.html](https://docs.python.org/3/library/csv.html)

## Major ecosystems

- **Django `QuerySet`** — lazily evaluated; `.iterator()` streams rows over
  a server-side cursor instead of caching the whole result: the
  page-hiding move at ORM scale.
  [docs.djangoproject.com/en/stable/ref/models/querysets/#iterator](https://docs.djangoproject.com/en/stable/ref/models/querysets/#iterator)
- **boto3 paginators** — AWS list APIs return truncated pages; a paginator
  wraps the continuation-token dance into one iterable, exactly this unit's
  `iterate_pages` shape.
  [boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html) *(unverified)*

## What to notice across all of them

Every one hides a *cursor protocol* (continuation tokens, DB cursors, file
offsets) behind the one protocol Python already speaks. And every one
documents its laziness as a feature with consequences — Django warns that
`.iterator()` skips caching; file iterators exhaust. When reviewing, ask:
does the signature promise `Iterator`, and does anything downstream silently
materialize it?
