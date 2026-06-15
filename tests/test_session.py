import pytest

from leftlevel_helix.identity import Identity
from leftlevel_helix.session import Envelope, HelixSession, accept_invite, create_invite, finalize_invite


def make_pair():
    alice_identity = Identity.generate()
    bob_identity = Identity.generate()
    draft = create_invite(alice_identity)
    response, bob = accept_invite(bob_identity, draft.invite)
    alice = finalize_invite(draft, response)
    return alice, bob


def test_alice_bob_roundtrip():
    alice, bob = make_pair()
    env = alice.seal(b"hello bob")
    assert bob.next_receive_mailbox() == env.mailbox_id
    assert bob.open(env) == b"hello bob"

    reply = bob.seal(b"hello alice")
    assert alice.next_receive_mailbox() == reply.mailbox_id
    assert alice.open(reply) == b"hello alice"


def test_replay_is_rejected():
    alice, bob = make_pair()
    env = alice.seal(b"one-time")
    assert bob.open(env) == b"one-time"
    with pytest.raises(ValueError, match="replay"):
        bob.open(env)


def test_tampering_is_rejected():
    alice, bob = make_pair()
    env = alice.seal(b"do not change")
    data = env.to_dict()
    data["ciphertext"] = data["ciphertext"][:-2] + "AA"
    with pytest.raises(Exception):
        bob.open(Envelope.from_dict(data))


def test_out_of_order_delivery_within_skip_window():
    alice, bob = make_pair()
    env1 = alice.seal(b"first")
    env2 = alice.seal(b"second")
    assert bob.open(env2) == b"second"
    assert bob.open(env1) == b"first"


def test_outside_skip_window_rejected_without_state_change():
    alice, bob = make_pair()
    messages = [alice.seal(f"msg-{i}".encode()) for i in range(bob.max_skip + 3)]
    with pytest.raises(ValueError, match="outside"):
        bob.open(messages[-1])
    assert bob.open(messages[0]) == b"msg-0"


def test_no_plaintext_in_envelope():
    alice, _bob = make_pair()
    secret = b"the launch code is 12345"
    env = alice.seal(secret)
    serialized = str(env.to_dict()).encode()
    assert secret not in serialized
    assert b"launch" not in serialized


def test_session_state_roundtrip():
    alice, bob = make_pair()
    restored_bob = HelixSession.from_state_dict(bob.to_state_dict())
    env = alice.seal(b"persistent session works")
    assert restored_bob.open(env) == b"persistent session works"


def test_skipped_keys_survive_session_state_roundtrip():
    alice, bob = make_pair()
    env1 = alice.seal(b"first")
    env2 = alice.seal(b"second")
    assert bob.open(env2) == b"second"
    restored = HelixSession.from_state_dict(bob.to_state_dict())
    assert restored.open(env1) == b"first"
