from __future__ import annotations

import os

import pytest

from leftlevel_helix.primitives import sha256


class FakeMlKem768PrivateKey:
    """Test-only KEM stand-in for CI runners without OpenSSL 3.5+ ML-KEM.

    This class is intentionally scoped to pytest via monkeypatching. Production
    code still uses leftlevel_helix.kem.MlKem768PrivateKey and must have a real
    OpenSSL provider with ML-KEM-768 support.
    """

    def __init__(self, private_pem: bytes):
        self.private_pem = private_pem

    @classmethod
    def generate(cls) -> "FakeMlKem768PrivateKey":
        return cls(b"TEST-ONLY-FAKE-MLKEM-PRIVATE:" + os.urandom(32))

    def public_pem(self) -> bytes:
        return b"TEST-ONLY-FAKE-MLKEM-PUBLIC:" + sha256(self.private_pem)

    def decapsulate(self, ciphertext: bytes) -> bytes:
        return sha256(b"TEST-ONLY-FAKE-MLKEM-SHARED:" + ciphertext)


def fake_mlkem768_encapsulate(public_pem: bytes) -> tuple[bytes, bytes]:
    _ = public_pem
    ciphertext = b"TEST-ONLY-FAKE-MLKEM-CT:" + os.urandom(32)
    shared_secret = sha256(b"TEST-ONLY-FAKE-MLKEM-SHARED:" + ciphertext)
    return ciphertext, shared_secret


@pytest.fixture(autouse=True)
def use_test_kem_for_protocol_unit_tests(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest):
    """Make protocol unit tests portable across GitHub-hosted runners.

    GitHub's default Ubuntu runners may not expose OpenSSL 3.5+ ML-KEM-768.
    The protocol/session tests are about transcript binding, ratcheting,
    replay rejection, out-of-order delivery, and serialization. Those should run
    everywhere. The real OpenSSL ML-KEM integration test is marked real_mlkem and
    is not monkeypatched by this fixture.
    """

    if request.node.get_closest_marker("real_mlkem"):
        return

    import leftlevel_helix.session as session_module

    monkeypatch.setattr(session_module, "MlKem768PrivateKey", FakeMlKem768PrivateKey)
    monkeypatch.setattr(session_module, "mlkem768_encapsulate", fake_mlkem768_encapsulate)
