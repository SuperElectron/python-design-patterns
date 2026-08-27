# Facade — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing facade-shaped code.

## Python standard library

- **`subprocess.run`.** One call fronting `Popen`'s pipes, waiting, timeout,
  and return-code checking; `Popen` stays public for streaming callers.
  [docs.python.org/3/library/subprocess.html#subprocess.run](https://docs.python.org/3/library/subprocess.html#subprocess.run)
- **`shutil.make_archive`.** Walks the tree, creates the archive, writes
  entries, closes handles — the whole `zipfile`/`tarfile` dance in one call,
  with both modules importable beside it.
  [docs.python.org/3/library/shutil.html#shutil.make_archive](https://docs.python.org/3/library/shutil.html#shutil.make_archive)
- **`urllib.request.urlopen`.** Hides the opener/handler chain construction
  every request needs; `build_opener` remains for callers who want the knobs.
  [docs.python.org/3/library/urllib.request.html#urllib.request.urlopen](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen)

## Major ecosystems

- **`requests`' functional API.** `requests.get(url)` fronts
  Session/adapter/urllib3 machinery; the `Session` object is one import away
  when you need pooling or retries.
  [requests.readthedocs.io/en/latest/api/#main-interface](https://requests.readthedocs.io/en/latest/api/#main-interface)

## What to notice across all of them

Each facade owns a *policy*, not just a shortcut: `subprocess.run` decides
how waiting and non-zero exits work; `urlopen` decides the default handler
chain. And each leaves the machinery public — the measure of a good facade
is that power users never have to fight it.
