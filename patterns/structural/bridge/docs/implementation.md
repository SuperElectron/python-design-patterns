# Bridge — putting it into a system

## The smell it fixes

A class name with two axes baked into it — and a hierarchy that doubles every
time either axis grows:

```python
class EmailAlert: ...


class SlackAlert: ...


class SmsAlert: ...


class EmailDigest: ...


class SlackDigest: ...


class SmsDigest: ...  # 2 kinds x 3 transports = 6 classes, and counting
```

Adding WhatsApp means three new classes; adding a weekly-report kind means
four. The bridge cuts the product into a sum: kinds hold a transport, and
"Slack digest" becomes `DigestNotifier(SlackTransport(), "#ops")`.

## Steps

1. **Find the two axes.** Ask "what varies about what we *say*?" and "what
   varies about how it's *delivered*?" If you can't fill both blanks, you
   don't need a bridge.
2. **Type the implementor axis as a `Protocol`.** Keep it minimal — one or
   two methods the abstraction actually calls (`deliver(recipient, text)`).
3. **Make abstractions hold, not inherit.** Each kind is a dataclass with a
   `transport` field; behavior methods call through it.
4. **Inject at the edge.** Which transport a given notifier gets is wiring —
   configuration, DI, or a registry — never a hard-coded constructor default.
5. **Test the axes separately, then one combination.** Transports get their
   own tests; kinds are tested against a recording fake; a single M × N
   sweep pins that any pair composes.

```python
from patterns.structural.bridge import AlertNotifier, SlackTransport

notifier = AlertNotifier(SlackTransport(), "#ops")  # any kind x any transport
notifier.alert("critical", "db pool exhausted")
```

## Python idioms that keep it small

- **`Protocol` on the implementor axis** — backends satisfy it structurally;
  third parties can add transports without importing your base class.
- **Frozen dataclasses for abstractions** — the bridge reference is visible
  in the signature and immutable after wiring.
- **A callable as the degenerate implementor.** When the interface is one
  method, `Callable[[str, str], None]` may replace the Protocol entirely.

## Pitfalls

- **Bridging one axis.** If every "abstraction" is the same class with a
  different name, you only had implementors — use plain injection and stop.
- **A fat implementor interface.** The Protocol should carry what all
  backends share; per-backend extras belong on the backend, reached
  explicitly, or the axes are lying.
- **Leaking backend types through the abstraction** (returning a Slack
  response object from `alert`) re-couples what the bridge separated.
- **Hard-coding a default transport** in the abstraction — it silently turns
  the bridge back into a single-axis class.

## Worked example

[`examples/notification_center/`](../examples/notification_center/) routes
alerts and digests for three teams over three transports — run it with:

```bash
uv run python -m patterns.structural.bridge.examples.notification_center.main
```
