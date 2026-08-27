"""Behavioral tests for all three facade variants."""

import tempfile
import zipfile
from pathlib import Path

import pytest

from patterns.structural.facade import naive, pythonic, real_world


class TestNaive:
    def test_one_call_runs_the_whole_sequence(self) -> None:
        steps = naive.HomeTheaterFacade().watch_movie()
        assert steps == ["lights 10%", "projector on", "16:9", "amp on", "volume 5"]


class TestPythonic:
    def _subsystem(
        self,
    ) -> tuple[pythonic.Warehouse, pythonic.PaymentGateway, pythonic.Shipping, pythonic.Notifier]:
        return (
            pythonic.Warehouse(stock={"mug": 10}),
            pythonic.PaymentGateway(),
            pythonic.Shipping(),
            pythonic.Notifier(),
        )

    def test_facade_runs_every_step_in_order(self) -> None:
        warehouse, gateway, shipping, notifier = self._subsystem()
        result = pythonic.place_order(
            warehouse,
            gateway,
            shipping,
            notifier,
            sku="mug",
            quantity=2,
            price_cents=1200,
            card="4242",
            address="12 Grace Ave",
        )
        assert warehouse.stock["mug"] == 8
        assert gateway.charges == [("4242", 2400)]
        assert result.shipping_label in shipping.labels
        assert notifier.sent and result.transaction_id in notifier.sent[0]

    def test_declined_payment_rolls_back_the_reservation(self) -> None:
        warehouse, gateway, shipping, notifier = self._subsystem()
        gateway.declined_cards.add("0000")
        with pytest.raises(PermissionError):
            pythonic.place_order(
                warehouse,
                gateway,
                shipping,
                notifier,
                sku="mug",
                quantity=3,
                price_cents=1200,
                card="0000",
                address="x",
            )
        assert warehouse.stock["mug"] == 10  # released, not leaked
        assert shipping.labels == [] and notifier.sent == []

    def test_insufficient_stock_charges_nothing(self) -> None:
        warehouse, gateway, shipping, notifier = self._subsystem()
        with pytest.raises(LookupError):
            pythonic.place_order(
                warehouse,
                gateway,
                shipping,
                notifier,
                sku="mug",
                quantity=99,
                price_cents=1200,
                card="4242",
                address="x",
            )
        assert gateway.charges == []

    def test_subsystem_stays_public_for_full_control(self) -> None:
        # Invoice-only flow: callers can still drive the parts directly.
        gateway = pythonic.PaymentGateway()
        assert gateway.charge("4242", 500) == "txn-1"


class TestRealWorld:
    def test_make_archive_facade(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "src"
            source.mkdir()
            (source / "a.txt").write_text("hello")
            archive = real_world.archive_directory(source, Path(tmp))
            assert archive.exists()
            with zipfile.ZipFile(archive) as zf:
                assert zf.namelist() == ["a.txt"]
