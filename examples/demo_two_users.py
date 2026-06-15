from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from leftlevel_helix.identity import Identity
from leftlevel_helix.relay import BlindRelayStore
from leftlevel_helix.session import Envelope, accept_invite, create_invite, finalize_invite


def main() -> None:
    relay = BlindRelayStore()

    alice_identity = Identity.generate()
    bob_identity = Identity.generate()

    # Alice creates an invite. Bob accepts. Alice finalizes.
    draft = create_invite(alice_identity)
    response, bob_session = accept_invite(bob_identity, draft.invite)
    alice_session = finalize_invite(draft, response)

    # Alice sends an encrypted envelope. Relay only sees a mailbox and ciphertext.
    envelope = alice_session.seal(b"Hello Bob. This is encrypted and relay-blind.")
    relay.put(envelope.mailbox_id, envelope.to_dict())

    fetched = relay.get_once(bob_session.next_receive_mailbox())
    assert fetched is not None
    plaintext = bob_session.open(Envelope.from_dict(fetched))
    print("Bob received:", plaintext.decode())

    # Bob replies.
    reply = bob_session.seal(b"Hi Alice. The server still cannot read this.")
    relay.put(reply.mailbox_id, reply.to_dict())
    fetched_reply = relay.get_once(alice_session.next_receive_mailbox())
    assert fetched_reply is not None
    reply_plaintext = alice_session.open(Envelope.from_dict(fetched_reply))
    print("Alice received:", reply_plaintext.decode())

    print("Relay audit snapshot after fetches:", relay.snapshot_for_audit())


if __name__ == "__main__":
    main()
