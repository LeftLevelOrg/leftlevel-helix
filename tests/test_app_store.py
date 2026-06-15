from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from leftlevel_helix.app_store import AppStore
from leftlevel_helix.client import HttpRelayClient
from leftlevel_helix.identity import Identity
from leftlevel_helix.session import accept_invite, create_invite, finalize_invite


class RelayHandler(BaseHTTPRequestHandler):
    store: dict[str, dict] = {}

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
            return
        prefix = "/v0/envelopes/"
        if self.path.startswith(prefix):
            mailbox_id = self.path[len(prefix):]
            envelope = self.store.pop(mailbox_id, None)
            self._send_json(200, {"found": envelope is not None, "envelope": envelope})
            return
        self._send_json(404, {"detail": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        envelope = json.loads(self.rfile.read(length).decode("utf-8"))
        self.store[envelope["mailbox_id"]] = envelope
        self._send_json(200, {"status": "stored"})


def make_pair():
    alice_identity = Identity.generate()
    bob_identity = Identity.generate()
    draft = create_invite(alice_identity)
    response, bob = accept_invite(bob_identity, draft.invite)
    alice = finalize_invite(draft, response)
    return alice, bob


def test_app_store_contacts_and_history(tmp_path):
    alice, _bob = make_pair()
    path = tmp_path / "store.llh.vault"
    store = AppStore.create(str(path), "correct horse battery")
    store.add_contact("bob", alice)
    store.record_message("bob", "sent", "hello")

    restored = AppStore.load(str(path), "correct horse battery")
    views = restored.contact_views()
    assert len(views) == 1
    assert views[0].name == "bob"
    assert views[0].trust_state == "unverified"
    assert views[0].sent == 1
    assert restored.history("bob")[0]["body"] == "hello"


def test_app_store_relay_product_flow(tmp_path):
    RelayHandler.store = {}
    server = ThreadingHTTPServer(("127.0.0.1", 0), RelayHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        relay_url = f"http://127.0.0.1:{server.server_port}"
        client = HttpRelayClient(relay_url)
        alice_session, bob_session = make_pair()
        alice_store = AppStore.create(str(tmp_path / "alice.llh.vault"), "correct horse battery")
        bob_store = AppStore.create(str(tmp_path / "bob.llh.vault"), "correct horse battery")
        alice_store.add_contact("bob", alice_session, verified=True)
        bob_store.add_contact("alice", bob_session, verified=True)

        alice = alice_store.load_session("bob")
        envelope = alice.seal(b"hello from product store")
        client.put_envelope(envelope)
        alice_store.save_session("bob", alice)
        alice_store.record_message("bob", "sent", "hello from product store", mailbox_id=envelope.mailbox_id)

        bob = bob_store.load_session("alice")
        fetched = client.fetch_once(bob.next_receive_mailbox())
        assert fetched is not None
        plaintext = bob.open(fetched).decode("utf-8")
        bob_store.save_session("alice", bob)
        bob_store.record_message("alice", "received", plaintext, mailbox_id=fetched.mailbox_id)

        assert plaintext == "hello from product store"
        assert alice_store.contact_views()[0].sent == 1
        assert bob_store.contact_views()[0].received == 1
        assert bob_store.history("alice")[0]["body"] == "hello from product store"
    finally:
        server.shutdown()
        thread.join(timeout=5)
