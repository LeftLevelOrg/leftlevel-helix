from __future__ import annotations

from dataclasses import dataclass

PAIRING_STATUS_VERSION = "LLH-PAIRING-STATUS-v0.1"


@dataclass(frozen=True)
class PairingStatus:
    v: str
    state: str
    label: str
    next_action: str
    blocks_friend_testing: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "v": self.v,
            "state": self.state,
            "label": self.label,
            "next_action": self.next_action,
            "blocks_friend_testing": self.blocks_friend_testing,
        }


def pairing_status_for_contact_count(contact_count: int) -> PairingStatus:
    if contact_count <= 0:
        return PairingStatus(
            v=PAIRING_STATUS_VERSION,
            state="needs_pairing",
            label="Pairing needed",
            next_action="Create or import a paired session before interface testing.",
            blocks_friend_testing=True,
        )
    return PairingStatus(
        v=PAIRING_STATUS_VERSION,
        state="paired_contacts_available",
        label="Paired contact available",
        next_action="Verify the safety number before sending sensitive messages.",
        blocks_friend_testing=False,
    )
