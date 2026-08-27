---
id: behavioral/template_method
name: Template Method
aliases: [hook-methods, skeleton-algorithm]
guide_url: null
problem: "Fix an algorithm's skeleton while letting callers vary individual steps."
symptoms: ["same steps, different details", "framework calls your overrides", "setUp/tearDown-style hooks"]
verdict: prefer-alternative
caveats:
  - "Passing step callables as keyword arguments with defaults does the same job without inheritance, and composes better."
  - "Subclass hooks make sense at framework boundaries (unittest, socketserver) where the framework owns the loop and you own the steps."
stdlib_sightings: [json.JSONEncoder.default, unittest.TestCase.setUp, socketserver.BaseRequestHandler.handle]
---

# Template Method

## Problem

Report generation always goes fetch → format → deliver, but each report
formats differently. The skeleton must stay fixed while steps vary.

## Naive solution

`naive.py` is the GoF form: the base class owns the skeleton as a concrete
method; subclasses override the abstract hook steps.

## Pythonic solution

The skeleton is a function; the varying steps are callable parameters with
defaults. No subclass per variation, and steps combine freely at call time.

## In the wild

`json.JSONEncoder` runs the encoding skeleton and calls your `default()`
hook for objects it can't serialize — a template method you've probably
already overridden. `unittest.TestCase.setUp`/`tearDown` and
`socketserver.BaseRequestHandler.handle` are the same shape.

## Verdict

**Prefer an alternative** in your own code — pass the steps. Recognize and
use the subclass form at framework boundaries.
