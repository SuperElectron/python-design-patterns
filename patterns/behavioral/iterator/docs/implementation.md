# Iterator — putting it into a system

## The smell it fixes

Pagination leaking everywhere: every caller of your API client repeats the
same `while page: fetch, extend, page += 1` dance — or worse, someone
"simplifies" it to `fetch_all()` and the service melts when a tenant has a
million records.

## Steps

1. **Find the traversal that callers keep re-implementing** (pages, DB
   cursors, chunked file reads, retry-and-continue scans).
2. **Write it once as a generator.** The generator owns the cursor,
   the stop condition, and nothing else:

   ```python
   from patterns.behavioral.iterator import iterate_pages


   def articles(self) -> Iterator[str]:
       return iterate_pages(self._backend.fetch)
   ```

3. **Return `Iterator[T]`, not `list[T]`.** The signature is the promise of
   laziness; a list return silently repeals it.
4. **Let callers bound the work** with `itertools.islice` / early `break` —
   that's the payoff; don't add a `limit=` parameter that re-implements it.
5. **Test the laziness, not just the items.** Log fetches in the fake
   backend and assert consuming 7 items touched 2 pages. If laziness is the
   contract, an eager regression must fail a test.

## Python idioms that keep it small

- `__iter__` **written as a generator** makes any class iterable in one
  line — no iterator class.
- **Compose, don't accumulate**: `islice(count(), …)`, `chain`, and
  generator expressions build pipelines where nothing runs until iteration.
- A generator that must clean up (close a cursor) should be consumed with
  `contextlib.closing` or wrapped in a context manager — say which in its
  docstring.

## Pitfalls

- **Iterators exhaust.** A generator iterates once; a second `for` gets
  nothing. Return a *fresh* iterator per call (as `articles()` does), and
  never stash a half-consumed one in shared state.
- **The container/iterator confusion**: the container's `__iter__` returns a
  fresh iterator; the iterator's `__iter__` returns itself. Swap them and
  nested loops break mysteriously.
- **Side effects in generators run late** (or never, if the caller stops
  early). Don't hide commits or releases inside a traversal.
- **`StopIteration` escaping a generator body** — say, from an unguarded
  `next()` call inside it — would silently end the generator; PEP 479
  converts that escape into a `RuntimeError` so the bug is loud. Guard
  inner `next()` calls with a default or `except StopIteration`.

## Worked example

[`examples/paginated_client/`](../examples/paginated_client/) applies every
step to an article API client with an observably lazy fetch log:

```bash
uv run python -m patterns.behavioral.iterator.examples.paginated_client
```
