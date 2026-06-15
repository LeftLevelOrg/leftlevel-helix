from __future__ import annotations

from leftlevel_helix.pairing_status import PAIRING_STATUS_VERSION, pairing_status_for_contact_count


def test_pairing_status_blocks_when_no_contacts():
    status = pairing_status_for_contact_count(0)

    assert status.v == PAIRING_STATUS_VERSION
    assert status.state == "needs_pairing"
    assert status.blocks_friend_testing is True
    assert "Create or import" in status.next_action


def test_pairing_status_allows_after_contact_exists():
    status = pairing_status_for_contact_count(1)

    assert status.state == "paired_contacts_available"
    assert status.blocks_friend_testing is False
    assert "Verify the safety number" in status.next_action
    assert status.to_dict()["label"] == "Paired contact available"
