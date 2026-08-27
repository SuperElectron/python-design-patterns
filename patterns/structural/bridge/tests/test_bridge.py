"""Behavioral tests for all three bridge variants."""

from patterns.structural.bridge import naive, pythonic, real_world


class TestNaive:
    def test_same_abstraction_different_implementations(self) -> None:
        assert naive.Circle(naive.VectorRenderer(), 2.0).draw() == "<circle r=2.0/>"
        assert "pixels" in naive.Circle(naive.RasterRenderer(), 2.0).draw()


class TestPythonic:
    def test_one_abstraction_over_two_transports(self) -> None:
        slack, email = pythonic.SlackTransport(), pythonic.EmailTransport()
        pythonic.AlertNotifier(slack, "#ops").alert("critical", "disk full")
        pythonic.AlertNotifier(email, "ops@x.com").alert("critical", "disk full")
        assert slack.posts == ["slack #ops: [CRITICAL] disk full"]
        assert email.outbox == ["email to ops@x.com: [CRITICAL] disk full"]

    def test_two_abstractions_over_one_transport(self) -> None:
        slack = pythonic.SlackTransport()
        pythonic.AlertNotifier(slack, "#ops").alert("warn", "slow queries")
        pythonic.DigestNotifier(slack, "#ops").digest(["a", "b"])
        assert len(slack.posts) == 2  # both sides vary independently

    def test_transport_specific_behavior_stays_in_the_transport(self) -> None:
        sms = pythonic.SmsTransport()
        pythonic.AlertNotifier(sms, "+1555").alert("info", "x" * 200)
        assert len(sms.messages[0]) <= len("sms +1555: ") + sms.MAX_LEN

    def test_any_duck_typed_transport_works(self) -> None:
        class Collector:
            def __init__(self) -> None:
                self.seen: list[str] = []

            def deliver(self, recipient: str, text: str) -> None:
                self.seen.append(text)

        collector = Collector()
        pythonic.AlertNotifier(collector, "anyone").alert("info", "hello")
        assert collector.seen == ["[INFO] hello"]


class TestRealWorld:
    def test_one_logger_call_reaches_both_implementations(self) -> None:
        a: list[str] = []
        b: list[str] = []
        real_world.logger_with_two_backends("bridge-test", a, b).info("msg")
        assert a == ["msg"] and b == ["msg"]
