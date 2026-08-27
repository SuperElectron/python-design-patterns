---
id: structural/adapter
name: Adapter
aliases: [wrapper, translator]
guide_url: null
problem: "Make an existing class usable through the interface your code expects, without editing either side."
symptoms: ["third-party API has the wrong shape", "legacy interface mismatch", "make X look like Y", "can't edit the class I'm given"]
verdict: pythonic
caveats:
  - "When the target interface is a single method, the adapter is just a function — don't build a class to hold one translation."
  - "Duck typing means the adapter only needs the methods your code actually calls, not the adaptee's whole surface."
stdlib_sightings: [io.TextIOWrapper, socket.makefile, functools.cmp_to_key]
---

# Adapter

## Problem

Your code speaks one interface; a class you cannot edit speaks another. A
sensor library reports Fahrenheit; your thermostat logic is written against
`celsius()`.

## Naive solution

`naive.py` is the GoF object adapter: a class implementing the target
interface, holding the adaptee, translating every call.

## Pythonic solution

Duck typing shrinks the job: adapt *only* what your code calls, and when
that's one method, a plain function is the whole adapter. `pythonic.py` shows
both the one-function adapter and a `__getattr__`-forwarding class for wider
surfaces.

## In the wild

`io.TextIOWrapper` adapts a binary stream to the text-file interface —
the stdlib's flagship adapter. `socket.makefile()` adapts a socket to a
file-like object; `functools.cmp_to_key` adapts old comparator functions to
the `key=` interface.

## Verdict

**Pythonic.** The honest way to reconcile interfaces you don't control.
