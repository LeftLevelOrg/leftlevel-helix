from __future__ import annotations

import json

import pytest

from leftlevel_helix.attachment_refs import reference_for_attachment
from leftlevel_helix.attachments import encrypt_attachment
from leftlevel_helix.attachment_transfer import OpaqueAttachmentPackage, relay_visible_fields, to_opaque_transfer_package


def test_transfer_package_hides_manifest_metadata():
    attachment = encrypt_attachment("sample.bin", b"payload", media_type="application/octet-stream", chunk_size=3)
    ref = reference_for_attachment(attachment)
    package = to_opaque_transfer_package(ref, attachment)
    encoded = json.dumps(package.to_dict())

    assert "sample.bin" not in encoded
    assert "application/octet-stream" not in encoded
    assert attachment.manifest.attachment_key not in encoded
    assert attachment.manifest.plaintext_sha256 not in encoded
    assert package.attachment_id == ref.attachment_id
    assert len(package.chunks) == ref.chunk_count


def test_transfer_package_roundtrip_shape():
    attachment = encrypt_attachment("sample.bin", b"payload", chunk_size=3)
    ref = reference_for_attachment(attachment)
    package = to_opaque_transfer_package(ref, attachment)
    restored = OpaqueAttachmentPackage.from_dict(package.to_dict())

    assert restored == package
    assert relay_visible_fields(restored) == {"v", "attachment_id", "chunks", "index", "nonce", "ciphertext", "ciphertext_sha256"}


def test_transfer_package_rejects_reference_mismatch():
    attachment = encrypt_attachment("sample.bin", b"payload", chunk_size=3)
    ref = reference_for_attachment(attachment)
    bad_ref = type(ref)(
        v=ref.v,
        attachment_version=ref.attachment_version,
        attachment_id=ref.attachment_id,
        file_name=ref.file_name,
        media_type=ref.media_type,
        total_size=ref.total_size,
        chunk_count=ref.chunk_count + 1,
        plaintext_sha256=ref.plaintext_sha256,
        manifest_sha256=ref.manifest_sha256,
        package_sha256=ref.package_sha256,
    )

    with pytest.raises(ValueError, match="chunk count"):
        to_opaque_transfer_package(bad_ref, attachment)
