from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as RealX25519PrivateKey

from leftlevel_helix.identity import Identity
from leftlevel_helix.primitives import sha256
from leftlevel_helix.session import Envelope, HelixSession, accept_invite, create_invite, finalize_invite
from leftlevel_helix.util import b64e

PLAINTEXT_001 = "hello from fixture"


class DeterministicBytes:
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.counter = 0

    def __call__(self, label: str, size: int) -> bytes:
        out = b""
        while len(out) < size:
            material = f"{self.namespace}|{label}|{self.counter}".encode("utf-8")
            out += sha256(material)
            self.counter += 1
        return out[:size]


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _identity_from_label(label: str) -> Identity:
    seed = sha256(f"LLH-FIXTURE-IDENTITY|{label}".encode("utf-8"))[:32]
    return Identity(Ed25519PrivateKey.from_private_bytes(seed))


def generate_vectors(output_dir: Path) -> Path:
    """Generate deterministic review fixtures for the current prototype.

    The monkeypatching in this function is test-only. It makes review fixtures
    reproducible without changing runtime randomness in the app/protocol code.
    """

    import leftlevel_helix.session as session_module

    source = DeterministicBytes("LLH-V0.6-FIXTURE")

    class DeterministicX25519PrivateKey:
        @staticmethod
        def generate():
            return RealX25519PrivateKey.from_private_bytes(source("x25519-private", 32))

        @staticmethod
        def from_private_bytes(data: bytes):
            return RealX25519PrivateKey.from_private_bytes(data)

    class FakeMlKem768PrivateKey:
        def __init__(self, private_pem: bytes):
            self.private_pem = private_pem

        @classmethod
        def generate(cls):
            return cls(b"TEST-ONLY-MLKEM-PRIVATE:" + source("mlkem-private", 32))

        def public_pem(self) -> bytes:
            return b"TEST-ONLY-MLKEM-PUBLIC:" + sha256(self.private_pem)

        def decapsulate(self, ciphertext: bytes) -> bytes:
            return sha256(b"TEST-ONLY-MLKEM-SHARED:" + ciphertext)

    def fake_mlkem768_encapsulate(public_pem: bytes) -> tuple[bytes, bytes]:
        _ = public_pem
        ciphertext = b"TEST-ONLY-MLKEM-CT:" + source("mlkem-ct", 32)
        shared_secret = sha256(b"TEST-ONLY-MLKEM-SHARED:" + ciphertext)
        return ciphertext, shared_secret

    original_x25519 = session_module.X25519PrivateKey
    original_kem_private = session_module.MlKem768PrivateKey
    original_kem_encapsulate = session_module.mlkem768_encapsulate
    original_random_bytes = session_module.random_bytes
    original_urandom = session_module.os.urandom

    try:
        session_module.X25519PrivateKey = DeterministicX25519PrivateKey
        session_module.MlKem768PrivateKey = FakeMlKem768PrivateKey
        session_module.mlkem768_encapsulate = fake_mlkem768_encapsulate
        session_module.random_bytes = lambda size: source("random-bytes", size)
        session_module.os.urandom = lambda size: source("padding", size)

        alice_identity = _identity_from_label("alice")
        bob_identity = _identity_from_label("bob")
        draft = create_invite(alice_identity)
        response, bob_session = accept_invite(bob_identity, draft.invite)
        alice_session = finalize_invite(draft, response)

        alice_session_start = alice_session.to_state_dict()
        bob_session_start = bob_session.to_state_dict()
        envelope = alice_session.seal(PLAINTEXT_001.encode("utf-8"), padding_block=256)
        opened = bob_session.open(envelope).decode("utf-8")
        if opened != PLAINTEXT_001:
            raise RuntimeError("fixture self-check failed")

        output_dir.mkdir(parents=True, exist_ok=True)
        _write_json(output_dir / "invite.json", draft.invite.to_dict())
        _write_json(output_dir / "response.json", response.to_dict())
        _write_json(output_dir / "alice_session_start.json", alice_session_start)
        _write_json(output_dir / "bob_session_start.json", bob_session_start)
        _write_json(output_dir / "envelope_001.json", envelope.to_dict())
        _write_json(output_dir / "alice_session_after_send.json", alice_session.to_state_dict())
        _write_json(output_dir / "bob_session_after_receive.json", bob_session.to_state_dict())

        expected = {
            "protocol": "LLH-HELIX-v0.2",
            "package_version": "0.6.0",
            "plaintext_001": PLAINTEXT_001,
            "safety_short_code": alice_session.safety_number().short_code,
            "safety_fingerprint": alice_session.safety_number().fingerprint,
            "visible_header_keys": sorted(envelope.header.keys()),
            "visible_header": envelope.header,
            "mailbox_id": envelope.mailbox_id,
            "ciphertext_sha256": b64e(sha256(envelope.ciphertext.encode("utf-8"))),
            "notes": "Generated with test-only deterministic helpers. Do not use fixture material in production.",
        }
        _write_json(output_dir / "expected.json", expected)
    finally:
        session_module.X25519PrivateKey = original_x25519
        session_module.MlKem768PrivateKey = original_kem_private
        session_module.mlkem768_encapsulate = original_kem_encapsulate
        session_module.random_bytes = original_random_bytes
        session_module.os.urandom = original_urandom

    return output_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate LeftLevel Helix protocol review fixtures.")
    parser.add_argument("--output", default="tests/fixtures/v0_6")
    args = parser.parse_args()
    out = generate_vectors(Path(args.output))
    print(f"wrote fixtures to {out}")


if __name__ == "__main__":
    main()
