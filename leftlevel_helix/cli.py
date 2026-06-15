from __future__ import annotations

import argparse
import json
import os
from getpass import getpass
from pathlib import Path

from .identity import Identity
from .session import (
    AliceDraft,
    Envelope,
    HelixInvite,
    HelixResponse,
    HelixSession,
    accept_invite,
    create_invite,
    finalize_invite,
)
from .vault import load_vault, save_vault


def _read_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


_CACHED_PASSPHRASE: str | None = None


def _passphrase(args: argparse.Namespace) -> str:
    global _CACHED_PASSPHRASE
    if getattr(args, "passphrase", None):
        return args.passphrase
    if os.environ.get("LLH_VAULT_PASSPHRASE"):
        return os.environ["LLH_VAULT_PASSPHRASE"]
    if _CACHED_PASSPHRASE is None:
        _CACHED_PASSPHRASE = getpass("Vault passphrase: ")
    return _CACHED_PASSPHRASE


def cmd_new_identity(args: argparse.Namespace) -> None:
    ident = Identity.generate()
    state = {"type": "identity", "identity_private": ident.export_private_b64()}
    if args.vault:
        save_vault(args.out, state, _passphrase(args))
    else:
        _write_json(args.out, state)
    print(f"created identity: {args.out}")


def _load_identity(path: str, args: argparse.Namespace) -> Identity:
    data = load_vault(path, _passphrase(args)) if path.endswith(".vault") else _read_json(path)
    if data.get("type") != "identity":
        raise SystemExit("identity file is not a LeftLevel identity")
    return Identity.import_private_b64(data["identity_private"])


def cmd_create_invite(args: argparse.Namespace) -> None:
    ident = _load_identity(args.identity, args)
    draft = create_invite(ident)
    # Draft contains private handshake material. Store in an encrypted vault.
    save_vault(args.draft, {"type": "alice_draft", "draft": draft.to_state_dict()}, _passphrase(args))
    _write_json(args.out, draft.invite.to_dict())
    print(f"created invite: {args.out}")
    print(f"saved encrypted draft: {args.draft}")


def cmd_accept_invite(args: argparse.Namespace) -> None:
    ident = _load_identity(args.identity, args)
    invite = HelixInvite.from_dict(_read_json(args.invite))
    response, session = accept_invite(ident, invite)
    _write_json(args.response, response.to_dict())
    save_vault(args.session, {"type": "session", "session": session.to_state_dict()}, _passphrase(args))
    print(f"created response: {args.response}")
    print(f"saved encrypted session: {args.session}")


def cmd_finalize_invite(args: argparse.Namespace) -> None:
    draft_data = load_vault(args.draft, _passphrase(args))
    if draft_data.get("type") != "alice_draft":
        raise SystemExit("draft file is not a LeftLevel draft")
    draft = AliceDraft.from_state_dict(draft_data["draft"])
    response = HelixResponse.from_dict(_read_json(args.response))
    session = finalize_invite(draft, response)
    save_vault(args.session, {"type": "session", "session": session.to_state_dict()}, _passphrase(args))
    print(f"saved encrypted session: {args.session}")


def _load_session(path: str, args: argparse.Namespace) -> HelixSession:
    data = load_vault(path, _passphrase(args))
    if data.get("type") != "session":
        raise SystemExit("session file is not a LeftLevel session")
    return HelixSession.from_state_dict(data["session"])


def _save_session(path: str, session: HelixSession, args: argparse.Namespace) -> None:
    save_vault(path, {"type": "session", "session": session.to_state_dict()}, _passphrase(args))


def cmd_seal(args: argparse.Namespace) -> None:
    session = _load_session(args.session, args)
    text = args.message
    if text is None and args.message_file:
        text = Path(args.message_file).read_text(encoding="utf-8")
    if text is None:
        raise SystemExit("provide --message or --message-file")
    envelope = session.seal(text.encode("utf-8"))
    _write_json(args.out, envelope.to_dict())
    _save_session(args.session, session, args)
    print(f"wrote encrypted envelope: {args.out}")


def cmd_open(args: argparse.Namespace) -> None:
    session = _load_session(args.session, args)
    envelope = Envelope.from_dict(_read_json(args.envelope))
    plaintext = session.open(envelope)
    _save_session(args.session, session, args)
    print(plaintext.decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(prog="leftlevel-helix")
    parser.add_argument("--passphrase", help="Vault passphrase. Prefer LLH_VAULT_PASSPHRASE or interactive prompt.")
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("new-identity")
    p.add_argument("--out", default="identity.llh.vault")
    p.add_argument("--vault", action="store_true", default=True)
    p.set_defaults(func=cmd_new_identity)

    p = sub.add_parser("create-invite")
    p.add_argument("--identity", required=True)
    p.add_argument("--out", default="invite.llh.json")
    p.add_argument("--draft", default="alice-draft.llh.vault")
    p.set_defaults(func=cmd_create_invite)

    p = sub.add_parser("accept-invite")
    p.add_argument("--identity", required=True)
    p.add_argument("--invite", required=True)
    p.add_argument("--response", default="response.llh.json")
    p.add_argument("--session", default="bob-session.llh.vault")
    p.set_defaults(func=cmd_accept_invite)

    p = sub.add_parser("finalize-invite")
    p.add_argument("--draft", required=True)
    p.add_argument("--response", required=True)
    p.add_argument("--session", default="alice-session.llh.vault")
    p.set_defaults(func=cmd_finalize_invite)

    p = sub.add_parser("seal")
    p.add_argument("--session", required=True)
    p.add_argument("--message")
    p.add_argument("--message-file")
    p.add_argument("--out", default="envelope.llh.json")
    p.set_defaults(func=cmd_seal)

    p = sub.add_parser("open")
    p.add_argument("--session", required=True)
    p.add_argument("--envelope", required=True)
    p.set_defaults(func=cmd_open)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
