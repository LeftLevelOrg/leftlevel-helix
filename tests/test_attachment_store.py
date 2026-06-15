from __future__ import annotations

import pytest

from leftlevel_helix.attachment_store import AttachmentStore


def test_attachment_store_roundtrip(tmp_path):
    path = tmp_path / "attachments.llh.vault"
    store = AttachmentStore.create(str(path), "correct horse battery")
    ref = store.add_bytes("sample.bin", b"payload", chunk_size=3)

    loaded = AttachmentStore.load(str(path), "correct horse battery")
    assert loaded.get_reference(ref.attachment_id) == ref
    assert loaded.decrypt(ref.attachment_id) == b"payload"


def test_attachment_store_lists_views(tmp_path):
    path = tmp_path / "attachments.llh.vault"
    store = AttachmentStore.create(str(path), "correct horse battery")
    ref = store.add_bytes("sample.bin", b"payload", chunk_size=3)

    views = store.list_attachments()
    assert len(views) == 1
    assert views[0].attachment_id == ref.attachment_id
    assert views[0].file_name == "sample.bin"
    assert views[0].total_size == len(b"payload")


def test_attachment_store_remove(tmp_path):
    path = tmp_path / "attachments.llh.vault"
    store = AttachmentStore.create(str(path), "correct horse battery")
    ref = store.add_bytes("sample.bin", b"payload")

    store.remove(ref.attachment_id)
    assert store.list_attachments() == []
    with pytest.raises(ValueError, match="unknown attachment"):
        store.get_reference(ref.attachment_id)


def test_attachment_store_rejects_wrong_passphrase(tmp_path):
    path = tmp_path / "attachments.llh.vault"
    store = AttachmentStore.create(str(path), "correct horse battery")
    store.add_bytes("sample.bin", b"payload")

    with pytest.raises(Exception):
        AttachmentStore.load(str(path), "wrong passphrase")
