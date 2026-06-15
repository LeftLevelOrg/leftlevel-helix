import pytest

from leftlevel_helix.identity import Identity
from leftlevel_helix.session import accept_invite, create_invite
from leftlevel_helix.verification import safety_number_from_handshake


def make_handshake():
    alice_identity = Identity.generate()
    bob_identity = Identity.generate()
    draft = create_invite(alice_identity)
    response, _bob = accept_invite(bob_identity, draft.invite)
    return draft.invite.to_dict(), response.to_dict()


def test_safety_number_is_stable_for_same_handshake():
    invite, response = make_handshake()
    first = safety_number_from_handshake(invite, response)
    second = safety_number_from_handshake(invite, response)
    assert first == second
    assert len(first.numeric.replace(" ", "")) == 30
    assert first.short_code.count("-") == 3


def test_safety_number_changes_for_different_handshakes():
    invite1, response1 = make_handshake()
    invite2, response2 = make_handshake()
    assert safety_number_from_handshake(invite1, response1) != safety_number_from_handshake(invite2, response2)


def test_safety_number_rejects_response_not_bound_to_invite():
    invite1, _response1 = make_handshake()
    _invite2, response2 = make_handshake()
    with pytest.raises(ValueError, match="different conversation"):
        safety_number_from_handshake(invite1, response2)
