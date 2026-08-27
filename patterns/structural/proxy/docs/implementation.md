# Proxy — putting it into a system

## The smell it fixes

Mediation logic fused into either the subject or every caller:

```python
class WarehouseConnection:
    def query(self, sql, *, role, audit_log):  # the subject now knows
        if role != "admin" and is_write(sql):  # about roles...
            raise PermissionError
        audit_log.append(sql)  # ...and about auditing
        ...
```

The connection's job is querying. Permissions and audit are *access*
concerns — they belong between the caller and the subject, in a layer each
side can ignore.

## Steps

1. **Name the mediation**: deferral, guarding, observation, remoteness. One
   proxy per concern — resist the mega-proxy with flags.
2. **Write each as a `__getattr__` forwarder** holding the subject (or its
   factory). Keep the proxy's own attributes few; `__getattr__` only fires
   for names not found on the proxy itself.
3. **Stack in the order the policy demands.** Outermost runs first:
   metering outside protection counts denied attempts; protection outside
   laziness means denied callers never pay construction.
   [`examples/db_gateway/`](../examples/db_gateway/) pins exactly that order.
4. **Keep a proxy-free path** for code that legitimately owns the subject —
   construction stays public, like any good facade or wrapper discipline.
5. **Test the mediation, not the forwarding**: assert the subject is *not*
   built before first use, denied roles *never* reach it, counts match
   traffic. Plain forwarding needs no tests of its own.

## Python idioms that keep it small

- **`__getattr__` (not `__getattribute__`)** — it fires only on lookup
  misses, so the proxy's own state stays reachable and recursion stays away.
- **`functools.cached_property`** when the mediation is "one expensive
  attribute, once" — the apparatus disappears into the stdlib.
- **`weakref.proxy`** when the mediation is lifetime, not access.
- **Factories, not eager subjects**, for virtual proxies: pass
  `lambda: Connection(dsn)`, never a pre-built connection.

## Pitfalls

- **The disguise is skin-deep** — `isinstance`, `is`, and every dunder
  bypass `__getattr__`. A proxied object that must support `len()`,
  iteration, or `with` needs those dunders written explicitly.
- **`__getattr__` recursion**: initialize the proxy's own attributes before
  any forwarding can happen, or route them through `object.__setattr__`.
- **Name shadowing**: an attribute the proxy defines (`access_counts`) wins
  over the subject's attribute of the same name — keep proxy surfaces tiny.
- **Leaking the subject**: a mediated method that returns `self._subject`
  hands callers an unguarded reference; return proxied results if the
  guarantee matters.

## Worked example

[`examples/db_gateway/`](../examples/db_gateway/) stacks metering over
role-protection over a lazy warehouse connection:

```bash
uv run python -m patterns.structural.proxy.examples.db_gateway.main
```
