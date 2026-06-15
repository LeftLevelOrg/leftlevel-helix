from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

PROTOCOL = b"LLH-HELIX-v0.2"


def random_bytes(n: int) -> bytes:
    return os.urandom(n)


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def hkdf(ikm: bytes, *, salt: bytes | None, info: bytes, length: int = 32) -> bytes:
    return HKDF(algorithm=hashes.SHA256(), length=length, salt=salt, info=PROTOCOL + b"|" + info).derive(ikm)


def hmac_sha256(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, PROTOCOL + b"|" + data, hashlib.sha256).digest()


@dataclass
class ChainStep:
    next_chain_key: bytes
    message_key: bytes
    nonce: bytes


def advance_chain(chain_key: bytes) -> ChainStep:
    """Advance a symmetric sending/receiving chain.

    The message key is single-use. The old chain key should be discarded by the caller.
    """
    message_key = hmac_sha256(chain_key, b"message-key")
    nonce = hmac_sha256(chain_key, b"nonce")[:12]
    next_chain_key = hmac_sha256(chain_key, b"next-chain")
    return ChainStep(next_chain_key=next_chain_key, message_key=message_key, nonce=nonce)


def aead_encrypt(key: bytes, nonce: bytes, plaintext: bytes, aad: bytes) -> bytes:
    return ChaCha20Poly1305(key).encrypt(nonce, plaintext, aad)


def aead_decrypt(key: bytes, nonce: bytes, ciphertext: bytes, aad: bytes) -> bytes:
    return ChaCha20Poly1305(key).decrypt(nonce, ciphertext, aad)
