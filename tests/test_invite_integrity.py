import pytest

from leftlevel_helix.identity import Identity
from leftlevel_helix.session import HelixInvite, accept_invite, create_invite


def test_invite_tamper_detected():
    alice = Identity.generate()
    bob = Identity.generate()
    draft = create_invite(alice)
    data = draft.invite.to_dict()
    data["body"] = dict(data["body"])
    data["body"]["conversation_id"] = "tampered"
    with pytest.raises(Exception):
        accept_invite(bob, HelixInvite.from_dict(data))
