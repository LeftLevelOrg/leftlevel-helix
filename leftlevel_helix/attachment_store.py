from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .attachment_refs import AttachmentReference, reference_for_attachment
from .attachments import EncryptedAttachment, decrypt_attachment, encrypt_attachment
from .vault import load_vault, save_vault

ATTACHMENT_STORE_VERSION = "LLH-ATTACHMENT-STORE-v0.1"


def new_attachment_store_state() -> dict[str, Any]:
    return {"v": ATTACHMENT_STORE_VERSION, "attachments": {}}


@dataclass(frozen=True)
class StoredAttachmentView:
    attachment_id: str
    file_name: str
    media_type: str
    total_size: int
    chunk_count: int
    plaintext_sha256: str


class AttachmentStore:
    """Encrypted local store for attachment packages."""

    def __init__(self, path: str, passphrase: str, state: dict[str, Any] | None = None):
        self.path = path
        self.passphrase = passphrase
        self.state = state if state is not None else new_attachment_store_state()
        if self.state.get("v") != ATTACHMENT_STORE_VERSION:
            raise ValueError("unsupported attachment store version")

    @classmethod
    def create(cls, path: str, passphrase: str) -> "AttachmentStore":
        store = cls(path, passphrase, new_attachment_store_state())
        store.save()
        return store

    @classmethod
    def load(cls, path: str, passphrase: str) -> "AttachmentStore":
        return cls(path, passphrase, load_vault(path, passphrase))

    def save(self) -> None:
        save_vault(self.path, self.state, self.passphrase)

    def add_bytes(self, file_name: str, data: bytes, *, media_type: str | None = None, chunk_size: int | None = None) -> AttachmentReference:
        kwargs: dict[str, Any] = {"media_type": media_type}
        if chunk_size is not None:
            kwargs["chunk_size"] = chunk_size
        attachment = encrypt_attachment(file_name, data, **kwargs)
        return self.add_attachment(attachment)

    def add_attachment(self, attachment: EncryptedAttachment) -> AttachmentReference:
        ref = reference_for_attachment(attachment)
        self.state["attachments"][ref.attachment_id] = {
            "reference": ref.to_dict(),
            "package": attachment.to_dict(),
        }
        self.save()
        return ref

    def get_reference(self, attachment_id: str) -> AttachmentReference:
        return AttachmentReference.from_dict(self._record(attachment_id)["reference"])

    def get_attachment(self, attachment_id: str) -> EncryptedAttachment:
        return EncryptedAttachment.from_dict(self._record(attachment_id)["package"])

    def decrypt(self, attachment_id: str) -> bytes:
        return decrypt_attachment(self.get_attachment(attachment_id))

    def list_attachments(self) -> list[StoredAttachmentView]:
        views: list[StoredAttachmentView] = []
        for attachment_id, record in sorted(self.state["attachments"].items()):
            ref = AttachmentReference.from_dict(record["reference"])
            views.append(
                StoredAttachmentView(
                    attachment_id=attachment_id,
                    file_name=ref.file_name,
                    media_type=ref.media_type,
                    total_size=ref.total_size,
                    chunk_count=ref.chunk_count,
                    plaintext_sha256=ref.plaintext_sha256,
                )
            )
        return views

    def remove(self, attachment_id: str) -> None:
        self._record(attachment_id)
        del self.state["attachments"][attachment_id]
        self.save()

    def _record(self, attachment_id: str) -> dict[str, Any]:
        try:
            return self.state["attachments"][attachment_id]
        except KeyError as exc:
            raise ValueError(f"unknown attachment: {attachment_id}") from exc
