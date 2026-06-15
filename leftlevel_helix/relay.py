from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from time import time
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MAILBOX_RE = re.compile(r"^[A-Za-z0-9_-]{20,80}$")
MAX_CIPHERTEXT_CHARS = 2_000_000


@dataclass
class BlindRelayStore:
    """A deliberately dumb relay store.

    It indexes encrypted envelopes by random-looking mailbox IDs only. It does
    not know users, conversations, or message plaintext. Production deployments
    should use encrypted-at-rest storage, short TTLs, rate limiting, and no IP logs.
    """

    ttl_seconds: int = 86_400
    max_items: int = 100_000
    items: dict[str, dict[str, Any]] = field(default_factory=dict)

    def put(self, mailbox_id: str, envelope: dict[str, Any]) -> None:
        self._gc()
        if len(self.items) >= self.max_items:
            raise ValueError("relay is at capacity")
        if mailbox_id in self.items:
            raise ValueError("mailbox already has an envelope")
        self.items[mailbox_id] = {"created_at": time(), "envelope": envelope}

    def get_once(self, mailbox_id: str) -> dict[str, Any] | None:
        self._gc()
        item = self.items.pop(mailbox_id, None)
        if item is None:
            return None
        return item["envelope"]

    def snapshot_for_audit(self) -> dict[str, Any]:
        """Return only what a compromised relay database would expose.

        This route is disabled by default in the FastAPI app. It is useful for
        development tests but should not be exposed in production.
        """
        self._gc()
        return {
            mid: {
                "created_at": value["created_at"],
                "stored_fields": list(value["envelope"].keys()),
                "ciphertext_len": len(value["envelope"].get("ciphertext", "")),
            }
            for mid, value in self.items.items()
        }

    def _gc(self) -> None:
        now = time()
        expired = [k for k, v in self.items.items() if now - v["created_at"] > self.ttl_seconds]
        for k in expired:
            self.items.pop(k, None)


class EnvelopeIn(BaseModel):
    mailbox_id: str = Field(min_length=20, max_length=80)
    header: dict[str, Any]
    ciphertext: str = Field(min_length=1, max_length=MAX_CIPHERTEXT_CHARS)


class FetchOut(BaseModel):
    found: bool
    envelope: dict[str, Any] | None = None


def _validate_mailbox_id(mailbox_id: str) -> None:
    if not MAILBOX_RE.match(mailbox_id):
        raise HTTPException(status_code=400, detail="invalid mailbox id")


def create_app(store: BlindRelayStore | None = None, *, enable_audit: bool | None = None) -> FastAPI:
    relay = store or BlindRelayStore()
    audit_enabled = enable_audit if enable_audit is not None else os.environ.get("LLH_ENABLE_AUDIT") == "1"
    app = FastAPI(title="LeftLevel Helix Blind Relay", version="0.2.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v0/envelopes")
    def put_envelope(envelope: EnvelopeIn) -> dict[str, str]:
        _validate_mailbox_id(envelope.mailbox_id)
        if envelope.mailbox_id != envelope.header.get("mailbox_id"):
            raise HTTPException(status_code=400, detail="mailbox mismatch")
        try:
            relay.put(envelope.mailbox_id, envelope.model_dump())
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return {"status": "stored"}

    @app.get("/v0/envelopes/{mailbox_id}", response_model=FetchOut)
    def fetch_envelope(mailbox_id: str) -> FetchOut:
        _validate_mailbox_id(mailbox_id)
        envelope = relay.get_once(mailbox_id)
        return FetchOut(found=envelope is not None, envelope=envelope)

    if audit_enabled:
        @app.get("/v0/audit")
        def audit() -> dict[str, Any]:
            return relay.snapshot_for_audit()

    return app


app = create_app()
