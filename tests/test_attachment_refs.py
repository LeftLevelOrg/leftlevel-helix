from __future__ import annotations

import pytest

from leftlevel_helix.attachment_refs import AttachmentMessagePayload, AttachmentReference, reference_for_attachment
from leftlevel_helix.attachments import encrypt_attachment


def test_attachment_reference_roundtrip():
    attachment = encrypt_attachment("sample.bin", b"sample bytes", chunk_size=4)
    ref = reference_for_attachment(attachment)
    restored = AttachmentReference.from_dict(ref.to_dict())

    assert restored == ref
    assert restored.file_name == "sample.bin"
    assert restored.total_size == len(b"sample bytes")
    assert restored.chunk_count == attachment.manifest.chunk_count
    assert restored.attachment_id


def test_attachment_reference_changes_when_content_changes():
    first = reference_for_attachment(encrypt_attachment("a.bin", b"one", chunk_size=2))
    second = reference_for_attachment(encrypt_attachment("a.bin", b"two", chunk_size=2))

    assert first.attachment_id != second.attachment_id
    assert first.package_sha256 != second.package_sha256


def test_attachment_message_payload_roundtrip():
    attachment = encrypt_attachment("sample.bin", b"bytes", chunk_size=4)
    payload = AttachmentMessagePayload(text="caption", attachment=reference_for_attachment(attachment))
    restored = AttachmentMessagePayload.from_dict(payload.to_dict())

    assert restored == payload
    assert restored.to_dict()["type"] == "attachment-message-v1"


def test_attachment_message_payload_rejects_unknown_type():
    with pytest.raises(ValueError, match="unsupported"):
        AttachmentMessagePayload.from_dict({"type": "unknown", "attachment": {}})
