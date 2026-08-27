# Prototype — where it lives outside this repo

Cited, real implementations to study (or point an agent at) when designing or
reviewing template/clone-shaped code.

## Python standard library

- **The `copy` module.** `copy.copy` (shallow — nested mutables shared) and
  `copy.deepcopy` (whole object graph), plus the `__copy__`/`__deepcopy__`
  customization protocol: the Prototype pattern absorbed into the language.
  [docs.python.org/3/library/copy.html](https://docs.python.org/3/library/copy.html)
- **`dataclasses.replace`.** The stdlib's copy-with-changes — per-use
  customization of a frozen product in one expression.
  [docs.python.org/3/library/dataclasses.html#dataclasses.replace](https://docs.python.org/3/library/dataclasses.html#dataclasses.replace)
- **`functools.partial`.** A pre-configured constructor: the exemplar as a
  recipe rather than an instance.
  [docs.python.org/3/library/functools.html#functools.partial](https://docs.python.org/3/library/functools.html#functools.partial)

## Major ecosystems

- **Django forms.** Declared fields are deep-copied onto every form instance
  (`fields = copy.deepcopy(base_fields)`) — live prototypes, cloned per use so
  one form's mutation can't leak into the class. *(unverified source link)*
  [github.com/django/django/blob/main/django/forms/forms.py](https://github.com/django/django/blob/main/django/forms/forms.py)
- **pydantic `model_copy(update=...)`.** Copy-with-tweaks as a public API on
  every model — `replace` generalized to validation-aware models. *(unverified
  source link)*
  [docs.pydantic.dev/latest/concepts/models/](https://docs.pydantic.dev/latest/concepts/models/#model-copy)
- **The guide's chapter** on why the pattern targets languages without
  first-class classes.
  [python-patterns.guide/gang-of-four/prototype/](https://python-patterns.guide/gang-of-four/prototype/)

## What to notice across all of them

The stdlib keeps *copying* (the mechanism) and leaves *the menu of exemplars*
(the pattern's structure) to you — and everything modern expresses "start from
this, change that" as an expression returning a new object, never as mutation
of a shared template.
