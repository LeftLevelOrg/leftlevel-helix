from __future__ import annotations

from leftlevel_helix.app_store import AppStore
from leftlevel_helix.identity import Identity
from leftlevel_helix.local_api import LocalApiService, create_app
from leftlevel_helix.session import accept_invite, create_invite, finalize_invite


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


def test_local_api_routes_exist(tmp_path):
    path = tmp_path / "store.llh.vault"
    AppStore.create(str(path), "correct horse battery")
    app = create_app(LocalApiService(store_path=str(path), passphrase="correct horse battery"))
    routes = {route.path for route in app.routes}
    assert "/health" in routes
    assert "/contacts" in routes
    assert "/contacts/{name}/history" in routes
    assert "/contacts/{name}/rename" in routes
    assert "/contacts/{name}/verify" in routes
