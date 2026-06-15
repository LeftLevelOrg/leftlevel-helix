from __future__ import annotations

import json
from dataclasses import dataclass

from .attachments import ATTACHMENT_VERSION, EncryptedAttachment
from .primitives import sha256
from .util import b64e

ATTACHMENT_REFERENCE_VERSION = "LLH-ATTACHMENT-REF-v0.1"


def canonical_json(data: dict) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass(frozen=True)
class AttachmentReference:
    """Metadata intended to be carried inside a sealed message payload."""

    v: str
    attachment_version: str
    attachment_id: str
    file_name: str
    media_type: str
    total_size: int
    chunk_count: int
    plaintext_sha256: str
    manifest_sha256: str
    package_sha256: str

    def to_dict(self) -> dict:
        return {
            "v": self.v,
            "attachment_version": self.attachment_version,
            "attachment_id": self.attachment_id,
            "file_name": self.file_name,
            "media_type": self.media_type,
            "total_size": self.total_size,
            "chunk_count": self.chunk_count,
            "plaintext_sha256": self.plaintext_sha256,
            "manifest_sha256": self.manifest_sha256,
            "package_sha256": self.package_sha256,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AttachmentReference":
        return cls(
            v=str(data["v"]),
            attachment_version=str(data["attachment_version"]),
            attachment_id=str(data["attachment_id"]),
            file_name=str(data["file_name"]),
            media_type=str(data["media_type"]),
            total_size=int(data["total_size"]),
            chunk_count=int(data["chunk_count"]),
            plaintext_sha256=str(data["plaintext_sha256"]),
            manifest_sha256=str(data["manifest_sha256"]),
            package_sha256=str(data["package_sha256"]),
        )


@dataclass(frozen=True)
class AttachmentMessagePayload:
    """Message payload shape for sending an attachment reference in a sealed envelope."""

    text: str
    attachment: AttachmentReference

    def to_dict(self) -> dict:
        return {
            "type": "attachment-message-v1",
            "text": self.text,
            "attachment": self.attachment.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AttachmentMessagePayload":
        if data.get("type") != "attachment-message-v1":
            raise ValueError("unsupported attachment message payload type")
        return cls(text=str(data.get("text", "")), attachment=AttachmentReference.from_dict(data["attachment"]))


def reference_for_attachment(attachment: EncryptedAttachment) -> AttachmentReference:
    manifest = attachment.manifest
    manifest_dict = manifest.to_dict()
    package_dict = attachment.to_dict()
    manifest_digest = b64e(sha256(canonical_json(manifest_dict)))
    package_digest = b64e(sha256(canonical_json(package_dict)))
    attachment_id = b64e(sha256(f"{manifest_digest}|{package_digest}".encode("utf-8")))[:32]
    return AttachmentReference(
        v=ATTACHMENT_REFERENCE_VERSION,
        attachment_version=ATTACHMENT_VERSION,
        attachment_id=attachment_id,
        file_name=manifest.file_name,
        media_type=manifest.media_type,
        total_size=manifest.total_size,
        chunk_count=manifest.chunk_count,
        plaintext_sha256=manifest.plaintext_sha256,
        manifest_sha256=manifest_digest,
        package_sha256=package_digest,
    )
