from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .app_store import AppStore
from .client import HttpRelayClient


class RenameRequest(BaseModel):
    new_name: str


class SendRequest(BaseModel):
    message: str
    relay_url: str
    timeout: float = 10.0


class ReceiveRequest(BaseModel):
    relay_url: str
    timeout: float = 10.0


class LocalApiService:
    """Local UI API over the LeftLevel app store."""

    def __init__(self, *, store_path: str, passphrase: str):
        self.store_path = store_path
        self.passphrase = passphrase

    def _store(self) -> AppStore:
        return AppStore.load(self.store_path, self.passphrase)

    def health(self) -> dict[str, str]:
        return {"status": "ok", "component": "leftlevel-local-api"}

    def contacts(self) -> list[dict[str, Any]]:
        return [asdict(view) for view in self._store().contact_views()]

    def history(self, name: str) -> list[dict[str, Any]]:
        return self._store().history(name)

    def rename_contact(self, old_name: str, new_name: str) -> dict[str, str]:
        store = self._store()
        store.rename_contact(old_name, new_name)
        return {"status": "renamed", "old_name": old_name, "new_name": new_name}

    def verify_contact(self, name: str) -> dict[str, str]:
        store = self._store()
        store.set_trust_state(name, "verified")
        return {"status": "verified", "name": name}

    def send_message(self, name: str, message: str, *, relay_url: str, timeout: float = 10.0) -> dict[str, str]:
        store = self._store()
        session = store.load_session(name)
        envelope = session.seal(message.encode("utf-8"))
        HttpRelayClient(relay_url, timeout=timeout).put_envelope(envelope)
        store.save_session(name, session)
        store.record_message(name, "sent", message, mailbox_id=envelope.mailbox_id)
        return {"status": "sent", "name": name, "mailbox_id": envelope.mailbox_id}

    def receive_message(self, name: str, *, relay_url: str, timeout: float = 10.0) -> dict[str, Any]:
        store = self._store()
        session = store.load_session(name)
        mailbox_id = session.next_receive_mailbox()
        envelope = HttpRelayClient(relay_url, timeout=timeout).fetch_once(mailbox_id)
        if envelope is None:
            return {"status": "empty", "name": name, "mailbox_id": mailbox_id, "message": None}
        message = session.open(envelope).decode("utf-8")
        store.save_session(name, session)
        store.record_message(name, "received", message, mailbox_id=envelope.mailbox_id)
        return {"status": "received", "name": name, "mailbox_id": envelope.mailbox_id, "message": message}


def create_app(service: LocalApiService) -> FastAPI:
    app = FastAPI(title="LeftLevel Local API", version="0.1")

    def handle(fn):
        try:
            return fn()
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/health")
    def health():
        return service.health()

    @app.get("/contacts")
    def contacts():
        return handle(service.contacts)

    @app.get("/contacts/{name}/history")
    def history(name: str):
        return handle(lambda: service.history(name))

    @app.post("/contacts/{name}/rename")
    def rename_contact(name: str, request: RenameRequest):
        return handle(lambda: service.rename_contact(name, request.new_name))

    @app.post("/contacts/{name}/verify")
    def verify_contact(name: str):
        return handle(lambda: service.verify_contact(name))

    @app.post("/contacts/{name}/send")
    def send_message(name: str, request: SendRequest):
        return handle(lambda: service.send_message(name, request.message, relay_url=request.relay_url, timeout=request.timeout))

    @app.post("/contacts/{name}/receive")
    def receive_message(name: str, request: ReceiveRequest):
        return handle(lambda: service.receive_message(name, relay_url=request.relay_url, timeout=request.timeout))

    return app


def main() -> None:
    store_path = os.environ.get("LLH_APP_STORE", "leftlevel-app.llh.vault")
    passphrase = os.environ.get("LLH_VAULT_PASSPHRASE")
    if not passphrase:
        raise SystemExit("LLH_VAULT_PASSPHRASE is required")
    host = os.environ.get("LLH_LOCAL_API_HOST", "127.0.0.1")
    port = int(os.environ.get("LLH_LOCAL_API_PORT", "8790"))
    uvicorn.run(create_app(LocalApiService(store_path=store_path, passphrase=passphrase)), host=host, port=port)


if __name__ == "__main__":
    main()
