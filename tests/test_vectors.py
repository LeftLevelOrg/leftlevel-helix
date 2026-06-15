from __future__ import annotations

import json

from leftlevel_helix.session import Envelope, HelixSession
from scripts.generate_protocol_vectors import PLAINTEXT_001, generate_vectors


def _read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_vector_generator_roundtrip(tmp_path):
    out = generate_vectors(tmp_path / "v0_6")

    expected = _read_json(out / "expected.json")
    envelope = Envelope.from_dict(_read_json(out / "envelope_001.json"))
    bob_start = HelixSession.from_state_dict(_read_json(out / "bob_session_start.json"))

    assert expected["protocol"] == "LLH-HELIX-v0.2"
    assert expected["package_version"] == "0.6.0"
    assert expected["plaintext_001"] == PLAINTEXT_001
    assert expected["visible_header_keys"] == ["mailbox_id", "mode", "v"]
    assert envelope.header == expected["visible_header"]
    assert "direction" not in envelope.header
    assert "padding_block" not in envelope.header
    assert bob_start.open(envelope).decode("utf-8") == PLAINTEXT_001


def test_vector_generator_is_repeatable(tmp_path):
    first = generate_vectors(tmp_path / "first")
    second = generate_vectors(tmp_path / "second")

    assert _read_json(first / "expected.json") == _read_json(second / "expected.json")
    assert _read_json(first / "invite.json") == _read_json(second / "invite.json")
    assert _read_json(first / "response.json") == _read_json(second / "response.json")
    assert _read_json(first / "envelope_001.json") == _read_json(second / "envelope_001.json")
