from __future__ import annotations

from leftlevel_helix.app_store import AppStore
from leftlevel_helix.identity import Identity
from leftlevel_helix.local_api import LocalApiService, create_app
from leftlevel_helix.session import accept_invite, create_invite, finalize_invite


class FakeRelayClient:
    envelopes = []

    def __init__(self, relay_url: str, timeout: float = 10.0):
        self.relay_url = relay_url
        self.timeout = timeout

    def put_envelope(self, envelope):
        self.envelopes.append(envelope)

    def fetch_once(self, mailbox_id: str):
        for index, envelope in enumerate(self.envelopes):
            if envelope.mailbox_id == mailbox_id:
                return self.envelopes.pop(index)
        return None


def make_pair():
    alice_identity = Identity.generate()
    bob_identity = Identity.generate()
    draft = create_invite(alice_identity)
    response, bob = accept_invite(bob_identity, draft.invite)
    alice = finalize_invite(draft, response)
    return alice, bob


def test_local_api_service_contact_workflow(tmp_path):
    alice, _bob = make_pair()
    path = tmp_path / "store.llh.vault"
    store = AppStore.create(str(path), "correct horse battery")
    store.add_contact("bob", alice)

    service = LocalApiService(store_path=str(path), passphrase="correct horse battery")
    assert service.health()["status"] == "ok"
    assert service.contacts()[0]["name"] == "bob"
    assert service.contacts()[0]["trust_state"] == "unverified"

    assert service.verify_contact("bob") == {"status": "verified", "name": "bob"}
    assert service.contacts()[0]["trust_state"] == "verified"

    assert service.rename_contact("bob", "robert") == {"status": "renamed", "old_name": "bob", "new_name": "robert"}
    assert service.contacts()[0]["name"] == "robert"


def test_local_api_setup_status_ready(tmp_path):
    alice, _bob = make_pair()
    path = tmp_path / "store.llh.vault"
    store = AppStore.create(str(path), "correct horse battery")
    store.add_contact("bob", alice)

    service = LocalApiService(store_path=str(path), passphrase="correct horse battery")
    status = service.setup_status()

    assert status["status"] == "ready"
    assert status["store_exists"] is True
    assert status["contact_count"] == 1
    assert status["ready_for_interface_test"] is True
    assert status["pairing"]["state"] == "paired_contacts_available"
    assert status["pairing"]["blocks_friend_testing"] is False


def test_local_api_setup_status_missing_store(tmp_path):
    path = tmp_path / "missing.llh.vault"
    service = LocalApiService(store_path=str(path), passphrase="correct horse battery")

    status = service.setup_status()

    assert status["status"] == "missing_store"
    assert status["store_exists"] is False
    assert status["contact_count"] == 0
    assert status["ready_for_interface_test"] is False
    assert status["pairing"]["state"] == "needs_pairing"
    assert status["pairing"]["blocks_friend_testing"] is True


def test_local_api_service_send_records_history(tmp_path, monkeypatch):
    alice, _bob = make_pair()
    path = tmp_path / "store.llh.vault"
    store = AppStore.create(str(path), "correct horse battery")
    store.add_contact("bob", alice)
    FakeRelayClient.envelopes = []
    monkeypatch.setattr("leftlevel_helix.local_api.HttpRelayClient", FakeRelayClient)

    service = LocalApiService(store_path=str(path), passphrase="correct horse battery")
    result = service.send_message("bob", "hello", relay_url="http://relay.test", timeout=1.0)

    assert result["status"] == "sent"
    assert result["name"] == "bob"
    assert result["mailbox_id"]
    assert service.history("bob")[-1]["body"] == "hello"
    assert len(FakeRelayClient.envelopes) == 1


def test_local_api_service_receive_empty(tmp_path, monkeypatch):
    alice, _bob = make_pair()
    path = tmp_path / "store.llh.vault"
    store = AppStore.create(str(path), "correct horse battery")
    store.add_contact("bob", alice)
    FakeRelayClient.envelopes = []
    monkeypatch.setattr("leftlevel_helix.local_api.HttpRelayClient", FakeRelayClient)

    service = LocalApiService(store_path=str(path), passphrase="correct horse battery")
    result = service.receive_message("bob", relay_url="http://relay.test", timeout=1.0)

    assert result["status"] == "empty"
    assert result["message"] is None


def test_local_api_routes_exist(tmp_path):
    path = tmp_path / "store.llh.vault"
    AppStore.create(str(path), "correct horse battery")
    app = create_app(LocalApiService(store_path=str(path), passphrase="correct horse battery"))
    routes = {route.path for route in app.routes}
    assert "/health" in routes
    assert "/setup/status" in routes
    assert "/contacts" in routes
    assert "/contacts/{name}/history" in routes
    assert "/contacts/{name}/rename" in routes
    assert "/contacts/{name}/verify" in routes
    assert "/contacts/{name}/send" in routes
    assert "/contacts/{name}/receive" in routes
