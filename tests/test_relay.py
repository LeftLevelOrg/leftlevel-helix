from leftlevel_helix.identity import Identity
from leftlevel_helix.relay import BlindRelayStore
from leftlevel_helix.session import Envelope, accept_invite, create_invite, finalize_invite


def test_blind_relay_store_get_once_and_no_plaintext():
    alice_identity = Identity.generate()
    bob_identity = Identity.generate()
    draft = create_invite(alice_identity)
    response, bob = accept_invite(bob_identity, draft.invite)
    alice = finalize_invite(draft, response)

    relay = BlindRelayStore()
    plaintext = b"relay must never see this message"
    env = alice.seal(plaintext)
    relay.put(env.mailbox_id, env.to_dict())

    audit = str(relay.snapshot_for_audit()).encode()
    assert plaintext not in audit
    assert b"message" not in audit

    fetched = relay.get_once(bob.next_receive_mailbox())
    assert fetched is not None
    assert relay.get_once(bob.next_receive_mailbox()) is None
    assert bob.open(Envelope.from_dict(fetched)) == plaintext
