from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from .session import HelixSession
from .vault import load_vault, save_vault

APP_STORE_VERSION = "LLH-APP-STORE-v0.1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_store_state() -> dict[str, Any]:
    return {"v": APP_STORE_VERSION, "contacts": {}, "messages": []}


@dataclass
class ContactView:
    name: str
    trust_state: str
    safety_short_code: str
    peer_fingerprint: str
    sent: int
    received: int


class AppStore:
    """Encrypted local product store for contacts, sessions, and message history.

    The store is intentionally simple for the prototype: one encrypted vault file
    contains contacts, serialized session state, and a local message log. This is
    not a production database yet, but it makes the CLI behave like a small app
    rather than a loose collection of files.
    """

    def __init__(self, path: str, passphrase: str, state: dict[str, Any] | None = None):
        self.path = path
        self.passphrase = passphrase
        self.state = state if state is not None else new_store_state()
        if self.state.get("v") != APP_STORE_VERSION:
            raise ValueError("unsupported app store version")

    @classmethod
    def create(cls, path: str, passphrase: str) -> "AppStore":
        store = cls(path, passphrase, new_store_state())
        store.save()
        return store

    @classmethod
    def load(cls, path: str, passphrase: str) -> "AppStore":
        return cls(path, passphrase, load_vault(path, passphrase))

    def save(self) -> None:
        save_vault(self.path, self.state, self.passphrase)

    def add_contact(self, name: str, session: HelixSession, *, verified: bool = False) -> None:
        if not name or any(ch.isspace() for ch in name):
            raise ValueError("contact name must be non-empty and contain no spaces")
        safety = session.safety_number()
        self.state["contacts"][name] = {
            "session": session.to_state_dict(),
            "trust_state": "verified" if verified else "unverified",
            "safety_short_code": safety.short_code,
            "safety_numeric": safety.numeric,
            "safety_fingerprint": safety.fingerprint,
            "peer_fingerprint": session.peer_identity_fingerprint(),
            "created_at": utc_now(),
            "updated_at": utc_now(),
        }
        self.save()

    def set_trust_state(self, name: str, trust_state: str) -> None:
        if trust_state not in {"unverified", "verified", "changed"}:
            raise ValueError("trust state must be unverified, verified, or changed")
        contact = self._contact(name)
        contact["trust_state"] = trust_state
        contact["updated_at"] = utc_now()
        self.save()

    def load_session(self, name: str) -> HelixSession:
        return HelixSession.from_state_dict(self._contact(name)["session"])

    def save_session(self, name: str, session: HelixSession) -> None:
        contact = self._contact(name)
        new_safety = session.safety_number()
        if contact.get("safety_fingerprint") and contact["safety_fingerprint"] != new_safety.fingerprint:
            contact["trust_state"] = "changed"
        contact["session"] = session.to_state_dict()
        contact["safety_short_code"] = new_safety.short_code
        contact["safety_numeric"] = new_safety.numeric
        contact["safety_fingerprint"] = new_safety.fingerprint
        contact["updated_at"] = utc_now()
        self.save()

    def record_message(self, contact_name: str, direction: str, body: str, *, mailbox_id: str | None = None) -> None:
        if direction not in {"sent", "received"}:
            raise ValueError("direction must be sent or received")
        self.state["messages"].append(
            {
                "contact": contact_name,
                "direction": direction,
                "body": body,
                "mailbox_id": mailbox_id,
                "created_at": utc_now(),
            }
        )
        self.save()

    def contact_views(self) -> list[ContactView]:
        views: list[ContactView] = []
        for name, contact in sorted(self.state["contacts"].items()):
            sent = sum(1 for m in self.state["messages"] if m["contact"] == name and m["direction"] == "sent")
            received = sum(1 for m in self.state["messages"] if m["contact"] == name and m["direction"] == "received")
            views.append(
                ContactView(
                    name=name,
                    trust_state=contact["trust_state"],
                    safety_short_code=contact["safety_short_code"],
                    peer_fingerprint=contact["peer_fingerprint"],
                    sent=sent,
                    received=received,
                )
            )
        return views

    def history(self, name: str) -> list[dict[str, Any]]:
        self._contact(name)
        return [m for m in self.state["messages"] if m["contact"] == name]

    def _contact(self, name: str) -> dict[str, Any]:
        try:
            return self.state["contacts"][name]
        except KeyError as exc:
            raise ValueError(f"unknown contact: {name}") from exc
