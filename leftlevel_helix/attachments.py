from __future__ import annotations

import mimetypes
from dataclasses import dataclass

from .primitives import aead_decrypt, aead_encrypt, random_bytes, sha256
from .util import b64d, b64e

ATTACHMENT_VERSION = "LLH-ATTACHMENT-v0.1"
DEFAULT_CHUNK_SIZE = 1024 * 1024


@dataclass(frozen=True)
class AttachmentChunk:
    index: int
    size: int
    nonce: str
    ciphertext: str
    plaintext_sha256: str
    ciphertext_sha256: str

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "size": self.size,
            "nonce": self.nonce,
            "ciphertext": self.ciphertext,
            "plaintext_sha256": self.plaintext_sha256,
            "ciphertext_sha256": self.ciphertext_sha256,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AttachmentChunk":
        return cls(
            index=int(data["index"]),
            size=int(data["size"]),
            nonce=str(data["nonce"]),
            ciphertext=str(data["ciphertext"]),
            plaintext_sha256=str(data["plaintext_sha256"]),
            ciphertext_sha256=str(data["ciphertext_sha256"]),
        )


@dataclass(frozen=True)
class AttachmentManifest:
    v: str
    file_name: str
    media_type: str
    total_size: int
    chunk_size: int
    chunk_count: int
    plaintext_sha256: str
    attachment_key: str

    def to_dict(self) -> dict:
        return {
            "v": self.v,
            "file_name": self.file_name,
            "media_type": self.media_type,
            "total_size": self.total_size,
            "chunk_size": self.chunk_size,
            "chunk_count": self.chunk_count,
            "plaintext_sha256": self.plaintext_sha256,
            "attachment_key": self.attachment_key,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AttachmentManifest":
        return cls(
            v=str(data["v"]),
            file_name=str(data["file_name"]),
            media_type=str(data["media_type"]),
            total_size=int(data["total_size"]),
            chunk_size=int(data["chunk_size"]),
            chunk_count=int(data["chunk_count"]),
            plaintext_sha256=str(data["plaintext_sha256"]),
            attachment_key=str(data["attachment_key"]),
        )


@dataclass(frozen=True)
class EncryptedAttachment:
    manifest: AttachmentManifest
    chunks: list[AttachmentChunk]

    def to_dict(self) -> dict:
        return {
            "manifest": self.manifest.to_dict(),
            "chunks": [chunk.to_dict() for chunk in self.chunks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EncryptedAttachment":
        return cls(
            manifest=AttachmentManifest.from_dict(data["manifest"]),
            chunks=[AttachmentChunk.from_dict(chunk) for chunk in data["chunks"]],
        )


def _media_type_for_name(file_name: str) -> str:
    return mimetypes.guess_type(file_name)[0] or "application/octet-stream"


def _aad(manifest: AttachmentManifest, index: int) -> bytes:
    return f"{manifest.v}|{manifest.file_name}|{manifest.total_size}|{index}".encode("utf-8")


def encrypt_attachment(file_name: str, data: bytes, *, media_type: str | None = None, chunk_size: int = DEFAULT_CHUNK_SIZE) -> EncryptedAttachment:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    attachment_key = random_bytes(32)
    manifest = AttachmentManifest(
        v=ATTACHMENT_VERSION,
        file_name=file_name,
        media_type=media_type or _media_type_for_name(file_name),
        total_size=len(data),
        chunk_size=chunk_size,
        chunk_count=(len(data) + chunk_size - 1) // chunk_size if data else 1,
        plaintext_sha256=b64e(sha256(data)),
        attachment_key=b64e(attachment_key),
    )
    chunks: list[AttachmentChunk] = []
    if data:
        pieces = [data[offset : offset + chunk_size] for offset in range(0, len(data), chunk_size)]
    else:
        pieces = [b""]
    for index, piece in enumerate(pieces):
        nonce = random_bytes(12)
        ciphertext = aead_encrypt(attachment_key, nonce, piece, _aad(manifest, index))
        chunks.append(
            AttachmentChunk(
                index=index,
                size=len(piece),
                nonce=b64e(nonce),
                ciphertext=b64e(ciphertext),
                plaintext_sha256=b64e(sha256(piece)),
                ciphertext_sha256=b64e(sha256(ciphertext)),
            )
        )
    return EncryptedAttachment(manifest=manifest, chunks=chunks)


def decrypt_attachment(attachment: EncryptedAttachment) -> bytes:
    manifest = attachment.manifest
    if manifest.v != ATTACHMENT_VERSION:
        raise ValueError("unsupported attachment version")
    if len(attachment.chunks) != manifest.chunk_count:
        raise ValueError("attachment chunk count mismatch")
    key = b64d(manifest.attachment_key)
    plaintext_parts: list[bytes] = []
    for expected_index, chunk in enumerate(sorted(attachment.chunks, key=lambda item: item.index)):
        if chunk.index != expected_index:
            raise ValueError("attachment chunks must be contiguous")
        ciphertext = b64d(chunk.ciphertext)
        if b64e(sha256(ciphertext)) != chunk.ciphertext_sha256:
            raise ValueError("attachment ciphertext checksum mismatch")
        plaintext = aead_decrypt(key, b64d(chunk.nonce), ciphertext, _aad(manifest, chunk.index))
        if len(plaintext) != chunk.size:
            raise ValueError("attachment chunk size mismatch")
        if b64e(sha256(plaintext)) != chunk.plaintext_sha256:
            raise ValueError("attachment plaintext checksum mismatch")
        plaintext_parts.append(plaintext)
    data = b"".join(plaintext_parts)
    if len(data) != manifest.total_size:
        raise ValueError("attachment total size mismatch")
    if b64e(sha256(data)) != manifest.plaintext_sha256:
        raise ValueError("attachment checksum mismatch")
    return data
