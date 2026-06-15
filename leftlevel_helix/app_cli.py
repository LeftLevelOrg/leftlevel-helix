from __future__ import annotations

import argparse
import os
from getpass import getpass

from .app_store import AppStore
from .client import HttpRelayClient
from .vault import load_vault
from .session import HelixSession


def _passphrase(args: argparse.Namespace) -> str:
    if getattr(args, "passphrase", None):
        return args.passphrase
    if os.environ.get("LLH_VAULT_PASSPHRASE"):
        return os.environ["LLH_VAULT_PASSPHRASE"]
    return getpass("App store passphrase: ")


def _store(args: argparse.Namespace) -> AppStore:
    return AppStore.load(args.store, _passphrase(args))


def _load_session_vault(path: str, passphrase: str) -> HelixSession:
    data = load_vault(path, passphrase)
    if data.get("type") != "session":
        raise SystemExit("session file is not a LeftLevel session")
    return HelixSession.from_state_dict(data["session"])


def cmd_init(args: argparse.Namespace) -> None:
    AppStore.create(args.store, _passphrase(args))
    print(f"created app store: {args.store}")


def cmd_add_contact(args: argparse.Namespace) -> None:
    passphrase = _passphrase(args)
    store = AppStore.load(args.store, passphrase)
    session = _load_session_vault(args.session, passphrase)
    store.add_contact(args.name, session, verified=args.verified)
    safety = session.safety_number()
    print(f"added contact: {args.name}")
    print(f"trust: {'verified' if args.verified else 'unverified'}")
    print(f"safety: {safety.short_code}")


def cmd_rename_contact(args: argparse.Namespace) -> None:
    store = _store(args)
    store.rename_contact(args.old_name, args.new_name)
    print(f"renamed contact: {args.old_name} -> {args.new_name}")


def cmd_verify_contact(args: argparse.Namespace) -> None:
    store = _store(args)
    store.set_trust_state(args.name, "verified")
    print(f"marked verified: {args.name}")


def cmd_contacts(args: argparse.Namespace) -> None:
    store = _store(args)
    for view in store.contact_views():
        badge = {"verified": "OK", "unverified": "NEW", "changed": "CHANGED"}[view.trust_state]
        print(f"{badge:7} {view.name:20} safety={view.safety_short_code} sent={view.sent} received={view.received}")


def cmd_send(args: argparse.Namespace) -> None:
    store = _store(args)
    session = store.load_session(args.name)
    envelope = session.seal(args.message.encode("utf-8"))
    HttpRelayClient(args.relay_url, timeout=args.timeout).put_envelope(envelope)
    store.save_session(args.name, session)
    store.record_message(args.name, "sent", args.message, mailbox_id=envelope.mailbox_id)
    print(f"sent encrypted message to {args.name}")


def cmd_receive(args: argparse.Namespace) -> None:
    store = _store(args)
    session = store.load_session(args.name)
    mailbox_id = session.next_receive_mailbox()
    envelope = HttpRelayClient(args.relay_url, timeout=args.timeout).fetch_once(mailbox_id)
    if envelope is None:
        print("no message available")
        return
    plaintext = session.open(envelope).decode("utf-8")
    store.save_session(args.name, session)
    store.record_message(args.name, "received", plaintext, mailbox_id=envelope.mailbox_id)
    print(plaintext)


def cmd_history(args: argparse.Namespace) -> None:
    store = _store(args)
    for msg in store.history(args.name):
        arrow = ">" if msg["direction"] == "sent" else "<"
        print(f"{msg['created_at']} {arrow} {msg['body']}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="leftlevel-app")
    parser.add_argument("--store", default="leftlevel-app.llh.vault")
    parser.add_argument("--passphrase", help="App store passphrase. Prefer LLH_VAULT_PASSPHRASE or interactive prompt.")
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("init")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add-contact")
    p.add_argument("name")
    p.add_argument("--session", required=True)
    p.add_argument("--verified", action="store_true")
    p.set_defaults(func=cmd_add_contact)

    p = sub.add_parser("rename-contact")
    p.add_argument("old_name")
    p.add_argument("new_name")
    p.set_defaults(func=cmd_rename_contact)

    p = sub.add_parser("verify-contact")
    p.add_argument("name")
    p.set_defaults(func=cmd_verify_contact)

    p = sub.add_parser("contacts")
    p.set_defaults(func=cmd_contacts)

    p = sub.add_parser("send")
    p.add_argument("name")
    p.add_argument("message")
    p.add_argument("--relay-url", required=True)
    p.add_argument("--timeout", type=float, default=10.0)
    p.set_defaults(func=cmd_send)

    p = sub.add_parser("receive")
    p.add_argument("name")
    p.add_argument("--relay-url", required=True)
    p.add_argument("--timeout", type=float, default=10.0)
    p.set_defaults(func=cmd_receive)

    p = sub.add_parser("history")
    p.add_argument("name")
    p.set_defaults(func=cmd_history)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
