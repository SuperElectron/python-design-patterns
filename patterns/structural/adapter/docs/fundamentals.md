# Adapter — fundamentals

## Intent

Convert the interface of a class into the interface clients expect, so
classes that could not otherwise work together can — without editing either
side. You control neither the caller's shape nor the callee's; the adapter is
the one piece you do control.

## Participants

| Role | Classic (GoF) form | Python form |
|---|---|---|
| Target | Abstract class the client is written against | A `Protocol` (or just the duck-typed calls the client makes) |
| Adaptee | The class with the wrong interface | Same — the vendor SDK, legacy module, stdlib object you can't edit |
| Adapter | A class implementing Target, holding the Adaptee | A plain function when one method differs; a small class (see [`pattern/adapter.py`](../pattern/adapter.py)) for wider surfaces |
| Client | Calls Target methods only | Same — and never imports the adaptee |

## Mechanism

1. Write the target interface from the *client's* needs — only the calls it
   actually makes.
2. The adapter holds the adaptee and translates each target call: units,
   argument shapes, naming, and failure conventions.
3. The client is constructed with any adapter; swapping adaptees is now a
   wiring change, not an edit.

## The classic form, and what Python absorbs

The textbook object adapter builds a full class triangle even for one method:

```python
class Thermometer(ABC):  # Target, as an abstract class
    @abstractmethod
    def celsius(self) -> float: ...


class SensorAdapter(Thermometer):  # Adapter subclasses the Target
    def __init__(self, sensor: FahrenheitSensor) -> None:
        self._sensor = sensor

    def celsius(self) -> float:
        return (self._sensor.get_fahrenheit() - 32) * 5 / 9
```

Python absorbs most of that ceremony. Duck typing means there is no Target
class to subclass — the adapter only needs the methods the client calls. A
one-method mismatch collapses to a function returning a closure. And for wide
surfaces, `__getattr__` forwarding (what `DelegatingAdapter` packages) means
the adapter lists only the *differences*, never the whole interface.

## When to use it

- A third-party or legacy interface has the wrong shape and you can't (or
  shouldn't) edit it.
- Two vendors do the same job differently and the rest of the system should
  not know which one is wired in.

## When not to use it

- You own both sides — change one of them instead of adding a layer.
- The "adapter" starts adding behavior (retries, caching, validation) — that
  is Decorator or Proxy territory; keep translation pure.

## Verdict: pythonic

The honest way to reconcile interfaces you don't control. Size it to the
mismatch: function for one method, `DelegatingAdapter` subclass for a few,
and stop before it becomes a facade over many objects.
