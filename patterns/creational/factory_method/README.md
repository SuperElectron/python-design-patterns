---
id: creational/factory_method
name: Factory Method
aliases: [virtual-constructor, class-attribute-factory]
guide_url: https://python-patterns.guide/gang-of-four/factory-method/
problem: "Let a class defer which helper object it constructs, so subclasses or callers can substitute another."
symptoms: ["subclass to change what gets built", "framework builds objects the app must customize", "response_class-style override"]
verdict: prefer-alternative
caveats:
  - "The guide's dodge is Dependency Injection: if you already have the object, pass the object, not a method that builds it."
  - "When creation must stay inside the class, prefer a class attribute factory (override by assignment or subclass) over an abstract method — any callable can be plugged in."
stdlib_sightings: [http.client.HTTPConnection.response_class, json.JSONDecoder]
---

# Factory Method

## Problem

A class needs a helper object mid-work — an HTTP connection needs a response
object — and users must be able to substitute their own helper class without
rewriting the containing class.

## Naive solution

`naive.py` is the book's: an abstract creator with an abstract
`factory_method()`, and one subclass per helper choice. Note the cost — a
subclass per configuration, just to change one constructor call.

## Pythonic solution

The guide's ranking, in `pythonic.py`: (1) **dependency injection** — just
pass the helper in; (2) a **class attribute factory** — creation stays
internal, but overriding is assignment or a one-line subclass, and *any*
callable is accepted; (3) an **instance attribute factory** for per-object
overrides without any subclass at all.

## In the wild

`http.client.HTTPConnection.response_class` is the canonical class attribute
factory: subclass, point it at your response type, done. `json.JSONDecoder`
does the same with its parse hooks.

## Verdict

**Prefer an alternative:** inject the dependency; failing that, a class
attribute factory. The abstract-method form is Java with the serial numbers
filed off.
