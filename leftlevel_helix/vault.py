from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .primitives import random_bytes
from .util import b64d, b64e, canonical_json

VAULT_VERSION = "LLH-VAULT-v0.1"
DEFAULT_ITERATIONS = 300_000


class VaultError(RuntimeError):
    pass


@dataclass
class VaultEnvelope:
    v: str
    kdf: str
    iterations: int
    salt: str
    nonce: str
    ciphertext: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "v": self.v,
            "kdf": self.kdf,
            "iterations": self.iterations,
            "salt": self.salt,
            "nonce": self.nonce,
            "ciphertext": self.ciphertext,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VaultEnvelope":
        if data.get("v") != VAULT_VERSION:
            raise VaultError("unsupported vault version")
        if data.get("kdf") != "PBKDF2-HMAC-SHA256":
            raise VaultError("unsupported vault KDF")
        return cls(
            v=data["v"],
            kdf=data["kdf"],
            iterations=int(data["iterations"]),
            salt=data["salt"],
            nonce=data["nonce"],
            ciphertext=data["ciphertext"],
        )


def derive_vault_key(passphrase: str, salt: bytes, *, iterations: int = DEFAULT_ITERATIONS) -> bytes:
    if len(passphrase) < 12:
        raise VaultError("passphrase must be at least 12 characters")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(passphrase.encode("utf-8"))


def encrypt_state(state: dict[str, Any], passphrase: str, *, iterations: int = DEFAULT_ITERATIONS) -> VaultEnvelope:
    salt = random_bytes(16)
    nonce = random_bytes(12)
    key = derive_vault_key(passphrase, salt, iterations=iterations)
    aad = canonical_json({"v": VAULT_VERSION, "kdf": "PBKDF2-HMAC-SHA256", "iterations": iterations, "salt": b64e(salt)})
    plaintext = canonical_json(state)
    ciphertext = ChaCha20Poly1305(key).encrypt(nonce, plaintext, aad)
    return VaultEnvelope(
        v=VAULT_VERSION,
        kdf="PBKDF2-HMAC-SHA256",
        iterations=iterations,
        salt=b64e(salt),
        nonce=b64e(nonce),
        ciphertext=b64e(ciphertext),
    )


def decrypt_state(envelope: VaultEnvelope, passphrase: str) -> dict[str, Any]:
    salt = b64d(envelope.salt)
    nonce = b64d(envelope.nonce)
    key = derive_vault_key(passphrase, salt, iterations=envelope.iterations)
    aad = canonical_json({"v": envelope.v, "kdf": envelope.kdf, "iterations": envelope.iterations, "salt": envelope.salt})
    try:
        plaintext = ChaCha20Poly1305(key).decrypt(nonce, b64d(envelope.ciphertext), aad)
    except InvalidTag as exc:
        raise VaultError("vault authentication failed: wrong passphrase or modified file") from exc
    return json.loads(plaintext.decode("utf-8"))


def save_vault(path: str | Path, state: dict[str, Any], passphrase: str, *, iterations: int = DEFAULT_ITERATIONS) -> None:
    envelope = encrypt_state(state, passphrase, iterations=iterations)
    Path(path).write_text(json.dumps(envelope.to_dict(), indent=2), encoding="utf-8")


def load_vault(path: str | Path, passphrase: str) -> dict[str, Any]:
    envelope = VaultEnvelope.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
    return decrypt_state(envelope, passphrase)
