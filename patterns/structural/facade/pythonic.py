"""The pythonic facade: a module-level function with good defaults.

The subsystem is a small order-fulfillment flow -- inventory, payment,
shipping, notification -- four calls every checkout caller used to
copy-paste, in the right order, with the right rollback. ``place_order``
is the one-call common case; the subsystem stays public for callers who
need the full controls (partial shipments, invoice-only, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Warehouse:
    stock: dict[str, int] = field(default_factory=dict)

    def reserve(self, sku: str, quantity: int) -> None:
        if self.stock.get(sku, 0) < quantity:
            raise LookupError(f"insufficient stock for {sku}")
        self.stock[sku] -= quantity

    def release(self, sku: str, quantity: int) -> None:
        self.stock[sku] = self.stock.get(sku, 0) + quantity


@dataclass
class PaymentGateway:
    charges: list[tuple[str, int]] = field(default_factory=list)
    declined_cards: set[str] = field(default_factory=set)

    def charge(self, card: str, amount_cents: int) -> str:
        if card in self.declined_cards:
            raise PermissionError(f"card {card} declined")
        self.charges.append((card, amount_cents))
        return f"txn-{len(self.charges)}"


@dataclass
class Shipping:
    labels: list[str] = field(default_factory=list)

    def create_label(self, sku: str, address: str) -> str:
        label = f"label-{len(self.labels) + 1}:{sku}->{address}"
        self.labels.append(label)
        return label


@dataclass
class Notifier:
    sent: list[str] = field(default_factory=list)

    def confirm(self, address: str, txn: str, label: str) -> None:
        self.sent.append(f"to {address}: paid {txn}, ships as {label}")


@dataclass(frozen=True)
class OrderResult:
    transaction_id: str
    shipping_label: str


def place_order(
    warehouse: Warehouse,
    gateway: PaymentGateway,
    shipping: Shipping,
    notifier: Notifier,
    *,
    sku: str,
    quantity: int,
    price_cents: int,
    card: str,
    address: str,
) -> OrderResult:
    """The facade: the whole checkout dance, in the right order, with the
    rollback nobody remembers to write at the call site."""
    warehouse.reserve(sku, quantity)
    try:
        txn = gateway.charge(card, price_cents * quantity)
    except PermissionError:
        warehouse.release(sku, quantity)  # the step copy-paste always forgets
        raise
    # Honest boundary: a crash below this line leaves the charge captured.
    # Real systems make charge/label/notify a saga (compensate on failure)
    # or an idempotent retry -- the facade pattern doesn't solve that part.
    label = shipping.create_label(sku, address)
    notifier.confirm(address, txn, label)
    return OrderResult(transaction_id=txn, shipping_label=label)


def main() -> None:
    warehouse = Warehouse(stock={"mug": 10})
    result = place_order(
        warehouse,
        PaymentGateway(),
        Shipping(),
        Notifier(),
        sku="mug",
        quantity=2,
        price_cents=1200,
        card="4242",
        address="12 Grace Ave",
    )
    print(result)
    print(f"stock after: {warehouse.stock}")


if __name__ == "__main__":
    main()
