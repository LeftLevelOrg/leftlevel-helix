from __future__ import annotations

import pytest

from leftlevel_helix.attachments import EncryptedAttachment, decrypt_attachment, encrypt_attachment
from leftlevel_helix.util import b64d, b64e


def test_attachment_roundtrip_small_text():
    data = "Hello attachments 😊".encode("utf-8")
    attachment = encrypt_attachment("note.txt", data, chunk_size=8)

    assert attachment.manifest.file_name == "note.txt"
    assert attachment.manifest.media_type == "text/plain"
    assert attachment.manifest.total_size == len(data)
    assert attachment.manifest.chunk_count > 1
    assert decrypt_attachment(attachment) == data


def test_attachment_roundtrip_empty_file():
    attachment = encrypt_attachment("empty.bin", b"")

    assert attachment.manifest.total_size == 0
    assert attachment.manifest.chunk_count == 1
    assert attachment.chunks[0].size == 0
    assert decrypt_attachment(attachment) == b""


def test_attachment_roundtrip_dict_shape():
    original = encrypt_attachment("photo.png", b"not really a png", chunk_size=4)
    restored = EncryptedAttachment.from_dict(original.to_dict())

    assert restored.manifest.media_type == "image/png"
    assert restored.to_dict() == original.to_dict()
    assert decrypt_attachment(restored) == b"not really a png"


def test_attachment_detects_ciphertext_tamper():
    attachment = encrypt_attachment("file.bin", b"payload")
    data = attachment.to_dict()
    ciphertext = bytearray(b64d(data["chunks"][0]["ciphertext"]))
    ciphertext[0] ^= 1
    data["chunks"][0]["ciphertext"] = b64e(bytes(ciphertext))
    tampered = EncryptedAttachment.from_dict(data)

    with pytest.raises(ValueError, match="checksum"):
        decrypt_attachment(tampered)


def test_attachment_rejects_missing_chunk():
    attachment = encrypt_attachment("big.bin", b"abcdefghij", chunk_size=3)
    data = attachment.to_dict()
    data["chunks"] = data["chunks"][:-1]
    tampered = EncryptedAttachment.from_dict(data)

    with pytest.raises(ValueError, match="chunk count"):
        decrypt_attachment(tampered)


def test_attachment_requires_positive_chunk_size():
    with pytest.raises(ValueError, match="chunk_size"):
        encrypt_attachment("bad.bin", b"data", chunk_size=0)
