from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

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
        if self.path != "/v0/envelopes":
            self._send_json(404, {"detail": "not found"})
            return
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


def test_http_relay_client_roundtrip():
    RelayHandler.store = {}
    server = ThreadingHTTPServer(("127.0.0.1", 0), RelayHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        client = HttpRelayClient(base_url)
        assert client.health() == {"status": "ok"}

        alice, bob = make_pair()
        envelope = alice.seal(b"hello over http relay")
        client.put_envelope(envelope)

        fetched = client.fetch_once(bob.next_receive_mailbox())
        assert fetched is not None
        assert bob.open(fetched) == b"hello over http relay"
        assert client.fetch_once(bob.next_receive_mailbox()) is None
    finally:
        server.shutdown()
        thread.join(timeout=5)
