from __future__ import annotations

from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption

from .util import b64e, b64d


@dataclass
class Identity:
    """A local pseudonymous identity.

    This identity is not a phone number or email. It is just a signing keypair.
    A user can create many identities for different contexts.
    """

    signing_key: Ed25519PrivateKey

    @classmethod
    def generate(cls) -> "Identity":
        return cls(Ed25519PrivateKey.generate())

    def public_key_bytes(self) -> bytes:
        return self.signing_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)

    def sign(self, message: bytes) -> bytes:
        return self.signing_key.sign(message)

    def export_private_b64(self) -> str:
        return b64e(self.signing_key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption()))

    @classmethod
    def import_private_b64(cls, text: str) -> "Identity":
        return cls(Ed25519PrivateKey.from_private_bytes(b64d(text)))


def verify_signature(public_key_bytes: bytes, message: bytes, signature: bytes) -> None:
    Ed25519PublicKey.from_public_bytes(public_key_bytes).verify(signature, message)
