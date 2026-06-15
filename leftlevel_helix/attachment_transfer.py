from __future__ import annotations

from dataclasses import dataclass

from .attachment_refs import AttachmentReference
from .attachments import EncryptedAttachment, AttachmentChunk

TRANSFER_VERSION = "LLH-ATTACHMENT-TRANSFER-v0.1"


@dataclass(frozen=True)
class OpaqueAttachmentChunk:
    v: str
    attachment_id: str
    index: int
    nonce: str
    ciphertext: str
    ciphertext_sha256: str

    def to_dict(self) -> dict:
        return {
            "v": self.v,
            "attachment_id": self.attachment_id,
            "index": self.index,
            "nonce": self.nonce,
            "ciphertext": self.ciphertext,
            "ciphertext_sha256": self.ciphertext_sha256,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OpaqueAttachmentChunk":
        return cls(
            v=str(data["v"]),
            attachment_id=str(data["attachment_id"]),
            index=int(data["index"]),
            nonce=str(data["nonce"]),
            ciphertext=str(data["ciphertext"]),
            ciphertext_sha256=str(data["ciphertext_sha256"]),
        )


@dataclass(frozen=True)
class OpaqueAttachmentPackage:
    v: str
    attachment_id: str
    chunks: list[OpaqueAttachmentChunk]

    def to_dict(self) -> dict:
        return {
            "v": self.v,
            "attachment_id": self.attachment_id,
            "chunks": [chunk.to_dict() for chunk in self.chunks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OpaqueAttachmentPackage":
        return cls(
            v=str(data["v"]),
            attachment_id=str(data["attachment_id"]),
            chunks=[OpaqueAttachmentChunk.from_dict(chunk) for chunk in data["chunks"]],
        )


def to_opaque_transfer_package(reference: AttachmentReference, attachment: EncryptedAttachment) -> OpaqueAttachmentPackage:
    if reference.chunk_count != len(attachment.chunks):
        raise ValueError("reference and attachment chunk count mismatch")
    return OpaqueAttachmentPackage(
        v=TRANSFER_VERSION,
        attachment_id=reference.attachment_id,
        chunks=[_opaque_chunk(reference.attachment_id, chunk) for chunk in attachment.chunks],
    )


def _opaque_chunk(attachment_id: str, chunk: AttachmentChunk) -> OpaqueAttachmentChunk:
    return OpaqueAttachmentChunk(
        v=TRANSFER_VERSION,
        attachment_id=attachment_id,
        index=chunk.index,
        nonce=chunk.nonce,
        ciphertext=chunk.ciphertext,
        ciphertext_sha256=chunk.ciphertext_sha256,
    )


def relay_visible_fields(package: OpaqueAttachmentPackage) -> set[str]:
    fields = set(package.to_dict().keys())
    for chunk in package.chunks:
        fields.update(chunk.to_dict().keys())
    return fields
