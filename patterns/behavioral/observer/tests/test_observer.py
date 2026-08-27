"""Behavioral tests for all three observer variants."""

from patterns.behavioral.observer import naive, pythonic, real_world


class TestNaive:
    def test_all_attached_observers_are_notified(self) -> None:
        station, display, alarm = naive.WeatherStation(), naive.Display(), naive.AlarmLog(30.0)
        station.attach(display)
        station.attach(alarm)
        station.set_temperature(35.0)
        assert display.shown == 35.0
        assert alarm.alerts == [35.0]

    def test_detached_observer_stops_receiving(self) -> None:
        station, display = naive.WeatherStation(), naive.Display()
        station.attach(display)
        station.set_temperature(10.0)
        station.detach(display)
        station.set_temperature(99.0)
        assert display.shown == 10.0


class TestPythonic:
    def test_assignment_broadcasts_to_callables(self) -> None:
        station = pythonic.WeatherStation()
        seen: list[float] = []
        station.listeners.append(seen.append)
        station.temperature = 21.5
        assert seen == [21.5]
        assert station.temperature == 21.5

    def test_observer_may_unsubscribe_during_notification(self) -> None:
        station = pythonic.WeatherStation()

        def once(value: float) -> None:
            station.listeners.remove(once)

        station.listeners.append(once)
        station.temperature = 1.0  # must not blow up mid-iteration
        station.temperature = 2.0
        assert station.listeners == []


class TestRealWorld:
    def test_done_callbacks_fire_in_order(self) -> None:
        assert real_world.observe_completion() == ["log: 42", "metrics: 42"]

    def test_late_subscription(self) -> None:
        assert real_world.late_subscription_fires_immediately()
