from __future__ import annotations

import argparse
from pathlib import Path

from .client import HttpRelayClient
from .session import HelixSession
from .vault import load_vault, save_vault


def _load_session(path: str, passphrase: str) -> HelixSession:
    data = load_vault(path, passphrase)
    if data.get("type") != "session":
        raise SystemExit("session file is not a LeftLevel session")
    return HelixSession.from_state_dict(data["session"])


def _save_session(path: str, session: HelixSession, passphrase: str) -> None:
    save_vault(path, {"type": "session", "session": session.to_state_dict()}, passphrase)


def cmd_health(args: argparse.Namespace) -> None:
    print(HttpRelayClient(args.relay_url, timeout=args.timeout).health())


def cmd_send(args: argparse.Namespace) -> None:
    session = _load_session(args.session, args.passphrase)
    text = args.message
    if text is None and args.message_file:
        text = Path(args.message_file).read_text(encoding="utf-8")
    if text is None:
        raise SystemExit("provide --message or --message-file")
    envelope = session.seal(text.encode("utf-8"))
    HttpRelayClient(args.relay_url, timeout=args.timeout).put_envelope(envelope)
    _save_session(args.session, session, args.passphrase)
    print(f"posted encrypted envelope to relay mailbox: {envelope.mailbox_id}")


def cmd_receive(args: argparse.Namespace) -> None:
    session = _load_session(args.session, args.passphrase)
    mailbox_id = session.next_receive_mailbox()
    envelope = HttpRelayClient(args.relay_url, timeout=args.timeout).fetch_once(mailbox_id)
    if envelope is None:
        print("no message available")
        return
    plaintext = session.open(envelope)
    _save_session(args.session, session, args.passphrase)
    if args.out:
        Path(args.out).write_bytes(plaintext)
    else:
        print(plaintext.decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(prog="leftlevel-relay")
    parser.add_argument("--relay-url", required=True)
    parser.add_argument("--timeout", type=float, default=10.0)
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("health")
    p.set_defaults(func=cmd_health)

    p = sub.add_parser("send")
    p.add_argument("--session", required=True)
    p.add_argument("--passphrase", required=True)
    p.add_argument("--message")
    p.add_argument("--message-file")
    p.set_defaults(func=cmd_send)

    p = sub.add_parser("receive")
    p.add_argument("--session", required=True)
    p.add_argument("--passphrase", required=True)
    p.add_argument("--out")
    p.set_defaults(func=cmd_receive)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
