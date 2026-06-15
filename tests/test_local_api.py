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


def test_local_api_create_store_from_missing_path(tmp_path):
    path = tmp_path / "new" / "store.llh.vault"
    service = LocalApiService(store_path=str(path), passphrase="correct horse battery")

    result = service.create_store()

    assert result["status"] == "created"
    assert path.exists()
    assert result["setup"]["status"] == "empty_store"
    assert result["setup"]["store_exists"] is True
    assert result["setup"]["contact_count"] == 0


def test_local_api_create_store_is_idempotent(tmp_path):
    path = tmp_path / "store.llh.vault"
    AppStore.create(str(path), "correct horse battery")
    service = LocalApiService(store_path=str(path), passphrase="correct horse battery")

    result = service.create_store()

    assert result["status"] == "already_exists"
    assert result["setup"]["store_exists"] is True


def test_local_api_create_test_friend(tmp_path):
    path = tmp_path / "store.llh.vault"
    AppStore.create(str(path), "correct horse battery")
    service = LocalApiService(store_path=str(path), passphrase="correct horse battery")

    result = service.create_test_friend("demo-friend")

    assert result["status"] == "created"
    assert result["friend"] == "demo-friend"
    assert result["friend_peer"] == "demo-friend-peer"
    assert result["setup"]["status"] == "ready"
    assert result["setup"]["contact_count"] == 2
    assert {contact["name"] for contact in service.contacts()} == {"demo-friend", "demo-friend-peer"}


def test_local_api_pairing_actions_create_contacts(tmp_path):
    alice_path = tmp_path / "alice.llh.vault"
    bob_path = tmp_path / "bob.llh.vault"
    AppStore.create(str(alice_path), "correct horse battery")
    AppStore.create(str(bob_path), "correct horse battery")
    alice_api = LocalApiService(store_path=str(alice_path), passphrase="correct horse battery")
    bob_api = LocalApiService(store_path=str(bob_path), passphrase="correct horse battery")

    invite = alice_api.create_pairing_invite("bob")
    assert invite["status"] == "invite_created"
    assert invite["draft_id"]

    response = bob_api.accept_pairing_invite("alice", invite["invite"])
    assert response["status"] == "response_created"
    assert bob_api.contacts()[0]["name"] == "alice"

    final = alice_api.finalize_pairing_response(invite["draft_id"], "bob", response["response"])
    assert final["status"] == "paired"
    assert alice_api.contacts()[0]["name"] == "bob"
    assert alice_api.contacts()[0]["safety_short_code"] == bob_api.contacts()[0]["safety_short_code"]


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
    assert "/setup/create" in routes
    assert "/setup/test-friend" in routes
    assert "/pairing/invite" in routes
    assert "/pairing/accept" in routes
    assert "/pairing/finalize" in routes
    assert "/contacts" in routes
    assert "/contacts/{name}/history" in routes
    assert "/contacts/{name}/rename" in routes
    assert "/contacts/{name}/verify" in routes
    assert "/contacts/{name}/send" in routes
    assert "/contacts/{name}/receive" in routes
