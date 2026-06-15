from __future__ import annotations

import hashlib
import json

import pytest

from scripts.generate_artifact_manifest import MANIFEST_VERSION, build_manifest, write_manifest


def test_build_manifest_records_size_and_digest(tmp_path):
    artifact = tmp_path / "sample.txt"
    artifact.write_text("hello", encoding="utf-8")

    manifest = build_manifest([artifact], version="v0-test")

    assert manifest["v"] == MANIFEST_VERSION
    assert manifest["version"] == "v0-test"
    assert manifest["artifacts"][0]["path"] == str(artifact)
    assert manifest["artifacts"][0]["size_bytes"] == 5
    assert manifest["artifacts"][0]["sha256"] == hashlib.sha256(b"hello").hexdigest()


def test_write_manifest_outputs_json(tmp_path):
    artifact = tmp_path / "sample.txt"
    artifact.write_text("hello", encoding="utf-8")
    output = tmp_path / "manifest.json"

    write_manifest(build_manifest([artifact]), output)

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["v"] == MANIFEST_VERSION
    assert data["artifacts"][0]["sha256"] == hashlib.sha256(b"hello").hexdigest()


def test_build_manifest_rejects_non_file(tmp_path):
    with pytest.raises(ValueError, match="not a file"):
        build_manifest([tmp_path / "missing.whl"])
