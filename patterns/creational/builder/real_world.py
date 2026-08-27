"""The stdlib's builders.

``email.message.EmailMessage`` is assembled call by call -- headers by
item assignment, body by ``set_content`` -- and only serialized at the end.
That is the Builder-as-convenience the guide describes.
"""

from __future__ import annotations

from email.message import EmailMessage


def build_email(sender: str, to: str, subject: str, body: str) -> EmailMessage:
    """Staged assembly of an RFC 5322 message."""
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    return msg


def main() -> None:
    msg = build_email("a@example.com", "b@example.com", "hi", "Builder in the stdlib.\n")
    print(msg.as_string())


if __name__ == "__main__":
    main()
