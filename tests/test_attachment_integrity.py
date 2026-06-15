from __future__ import annotations

from dataclasses import replace

from leftlevel_helix.attachment_refs import reference_for_attachment
from leftlevel_helix.attachments import EncryptedAttachment, encrypt_attachment
from leftlevel_helix.attachment_integrity import verify_opaque_transfer, verify_received_attachment
from leftlevel_helix.attachment_transfer import OpaqueAttachmentPackage, to_opaque_transfer_package


def test_received_attachment_integrity_verified():
    attachment = encrypt_attachment("sample.bin", b"payload", chunk_size=3)
    ref = reference_for_attachment(attachment)

    report = verify_received_attachment(ref, attachment)

    assert report.status == "verified"
    assert report.code == "verified"
    assert "allow_open" in report.actions


def test_received_attachment_blocks_reference_mismatch():
    attachment = encrypt_attachment("sample.bin", b"payload", chunk_size=3)
    ref = reference_for_attachment(attachment)
    bad_ref = replace(ref, package_sha256="bad")

    report = verify_received_attachment(bad_ref, attachment)

    assert report.status == "blocked"
    assert report.code == "package_digest_mismatch"
    assert "block_open" in report.actions
    assert "request_resend" in report.actions


def test_opaque_transfer_integrity_verified():
    attachment = encrypt_attachment("sample.bin", b"payload", chunk_size=3)
    ref = reference_for_attachment(attachment)
    package = to_opaque_transfer_package(ref, attachment)

    report = verify_opaque_transfer(ref, package)

    assert report.status == "verified"
    assert report.code == "verified"


def test_opaque_transfer_blocks_ciphertext_checksum_mismatch():
    attachment = encrypt_attachment("sample.bin", b"payload", chunk_size=3)
    ref = reference_for_attachment(attachment)
    package = to_opaque_transfer_package(ref, attachment)
    data = package.to_dict()
    data["chunks"][0]["ciphertext_sha256"] = "bad"
    tampered = OpaqueAttachmentPackage.from_dict(data)

    report = verify_opaque_transfer(ref, tampered)

    assert report.status == "blocked"
    assert report.code == "ciphertext_checksum_mismatch"


def test_opaque_transfer_blocks_missing_chunk():
    attachment = encrypt_attachment("sample.bin", b"payload", chunk_size=3)
    ref = reference_for_attachment(attachment)
    package = to_opaque_transfer_package(ref, attachment)
    data = package.to_dict()
    data["chunks"] = data["chunks"][:-1]
    missing = OpaqueAttachmentPackage.from_dict(data)

    report = verify_opaque_transfer(ref, missing)

    assert report.status == "blocked"
    assert report.code == "chunk_count_mismatch"


def test_opaque_transfer_warns_on_relay_metadata_exposure():
    attachment = encrypt_attachment("sample.bin", b"payload", chunk_size=3)
    ref = reference_for_attachment(attachment)
    package = to_opaque_transfer_package(ref, attachment)
    data = package.to_dict()
    data["file_name"] = "sample.bin"
    exposed = OpaqueAttachmentPackage.from_dict(data)
    exposed_dict = exposed.to_dict()
    exposed_dict["file_name"] = "sample.bin"

    class PackageWithExtraField:
        v = exposed.v
        attachment_id = exposed.attachment_id
        chunks = exposed.chunks

        def to_dict(self):
            return exposed_dict

    report = verify_opaque_transfer(ref, PackageWithExtraField())

    assert report.status == "warning"
    assert report.code == "relay_metadata_exposure"
