from __future__ import annotations

import json
from dataclasses import dataclass

from .attachment_refs import AttachmentReference, canonical_json
from .attachments import EncryptedAttachment, decrypt_attachment
from .attachment_transfer import OpaqueAttachmentPackage, TRANSFER_VERSION
from .primitives import sha256
from .util import b64e, b64d

INTEGRITY_VERSION = "LLH-INTEGRITY-v0.1"


@dataclass(frozen=True)
class IntegrityReport:
    v: str
    status: str
    code: str
    message: str
    attachment_id: str | None
    actions: list[str]

    def to_dict(self) -> dict:
        return {
            "v": self.v,
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "attachment_id": self.attachment_id,
            "actions": self.actions,
        }


def ok_report(attachment_id: str, message: str = "Attachment integrity verified") -> IntegrityReport:
    return IntegrityReport(
        v=INTEGRITY_VERSION,
        status="verified",
        code="verified",
        message=message,
        attachment_id=attachment_id,
        actions=["allow_open", "show_verified"],
    )


def warning_report(attachment_id: str | None, code: str, message: str) -> IntegrityReport:
    return IntegrityReport(
        v=INTEGRITY_VERSION,
        status="warning",
        code=code,
        message=message,
        attachment_id=attachment_id,
        actions=["warn_user", "request_resend", "review_contact_safety"],
    )


def blocked_report(attachment_id: str | None, code: str, message: str) -> IntegrityReport:
    return IntegrityReport(
        v=INTEGRITY_VERSION,
        status="blocked",
        code=code,
        message=message,
        attachment_id=attachment_id,
        actions=["block_open", "delete_attachment", "request_resend", "review_contact_safety"],
    )


def verify_opaque_transfer(reference: AttachmentReference, package: OpaqueAttachmentPackage) -> IntegrityReport:
    if package.v != TRANSFER_VERSION:
        return blocked_report(package.attachment_id, "unsupported_transfer_version", "Unsupported attachment transfer version")
    if package.attachment_id != reference.attachment_id:
        return blocked_report(package.attachment_id, "attachment_id_mismatch", "Attachment identifier does not match the sealed reference")
    if len(package.chunks) != reference.chunk_count:
        return blocked_report(package.attachment_id, "chunk_count_mismatch", "Attachment chunk count does not match the sealed reference")
    expected_indexes = list(range(reference.chunk_count))
    actual_indexes = sorted(chunk.index for chunk in package.chunks)
    if actual_indexes != expected_indexes:
        return blocked_report(package.attachment_id, "chunk_index_mismatch", "Attachment chunks are missing, duplicated, or out of sequence")
    for chunk in package.chunks:
        ciphertext = b64d(chunk.ciphertext)
        if b64e(sha256(ciphertext)) != chunk.ciphertext_sha256:
            return blocked_report(package.attachment_id, "ciphertext_checksum_mismatch", "Encrypted attachment chunk checksum mismatch")
    encoded = json.dumps(package.to_dict(), sort_keys=True)
    for forbidden in ["file_name", "media_type", "attachment_key", "plaintext_sha256", "manifest_sha256", "package_sha256"]:
        if forbidden in encoded:
            return warning_report(package.attachment_id, "relay_metadata_exposure", "Relay-facing attachment package contains metadata that should remain sealed")
    return ok_report(package.attachment_id, "Relay-facing attachment package verified")


def verify_received_attachment(reference: AttachmentReference, attachment: EncryptedAttachment) -> IntegrityReport:
    manifest = attachment.manifest
    if reference.attachment_version != manifest.v:
        return blocked_report(reference.attachment_id, "attachment_version_mismatch", "Attachment version does not match the sealed reference")
    if reference.chunk_count != len(attachment.chunks):
        return blocked_report(reference.attachment_id, "chunk_count_mismatch", "Attachment chunk count does not match the sealed reference")
    manifest_digest = b64e(sha256(canonical_json(manifest.to_dict())))
    if manifest_digest != reference.manifest_sha256:
        return blocked_report(reference.attachment_id, "manifest_digest_mismatch", "Attachment manifest does not match the sealed reference")
    package_digest = b64e(sha256(canonical_json(attachment.to_dict())))
    if package_digest != reference.package_sha256:
        return blocked_report(reference.attachment_id, "package_digest_mismatch", "Attachment package does not match the sealed reference")
    try:
        plaintext = decrypt_attachment(attachment)
    except Exception:
        return blocked_report(reference.attachment_id, "decrypt_or_integrity_failure", "Attachment could not be decrypted or failed integrity checks")
    if b64e(sha256(plaintext)) != reference.plaintext_sha256:
        return blocked_report(reference.attachment_id, "plaintext_digest_mismatch", "Decrypted attachment does not match the sealed reference")
    return ok_report(reference.attachment_id)
