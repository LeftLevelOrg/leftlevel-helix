from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .identity import verify_signature
from .primitives import sha256
from .util import b64d, b64e, canonical_json


@dataclass(frozen=True)
class SafetyNumber:
    """Human-comparable verification code for a completed Helix handshake.

    This is not secret. Alice and Bob compare it out-of-band before trusting a
    new contact. If a network attacker creates two different handshakes to sit
    between them, Alice and Bob will see different safety numbers.
    """

    numeric: str
    short_code: str
    fingerprint: str


def _group_digits(text: str, group_size: int = 5) -> str:
    return " ".join(text[i : i + group_size] for i in range(0, len(text), group_size))


def _verify_invite(invite: dict[str, Any]) -> None:
    body = invite["body"]
    verify_signature(b64d(body["alice_identity_pub"]), canonical_json(body), b64d(invite["signature"]))


def _verify_response(response: dict[str, Any]) -> None:
    body = response["body"]
    verify_signature(b64d(body["bob_identity_pub"]), canonical_json(body), b64d(response["signature"]))


def safety_number_from_handshake(invite: dict[str, Any], response: dict[str, Any]) -> SafetyNumber:
    """Return a safety number for invite/response verification.

    The function verifies both self-signatures and checks that the response is
    bound to the exact invite. A mismatch or tamper attempt raises ValueError or
    the underlying signature-verification exception.
    """

    _verify_invite(invite)
    _verify_response(response)

    invite_body = invite["body"]
    response_body = response["body"]
    if response_body.get("conversation_id") != invite_body.get("conversation_id"):
        raise ValueError("response is for a different conversation")

    expected_invite_hash = b64e(sha256(canonical_json(invite)))
    if response_body.get("invite_hash") != expected_invite_hash:
        raise ValueError("response did not bind to this invite")

    transcript_hash = sha256(canonical_json({"invite": invite, "response": response}))
    material = b"|".join(
        [
            b"LLH-SAFETY-NUMBER-v1",
            invite_body["v"].encode("utf-8"),
            invite_body["conversation_id"].encode("utf-8"),
            b64d(invite_body["alice_identity_pub"]),
            b64d(response_body["bob_identity_pub"]),
            transcript_hash,
        ]
    )
    digest = sha256(material)
    number = str(int.from_bytes(digest[:16], "big") % 10**30).zfill(30)
    return SafetyNumber(
        numeric=_group_digits(number, 5),
        short_code="-".join(number[i : i + 3] for i in range(0, 12, 3)),
        fingerprint=b64e(digest),
    )


def session_safety_number(*, protocol_name: str, conversation_id: str, alice_identity_pub: bytes, bob_identity_pub: bytes, transcript_hash: bytes) -> SafetyNumber:
    material = b"|".join(
        [
            b"LLH-SAFETY-NUMBER-v1",
            protocol_name.encode("utf-8"),
            conversation_id.encode("utf-8"),
            alice_identity_pub,
            bob_identity_pub,
            transcript_hash,
        ]
    )
    digest = sha256(material)
    number = str(int.from_bytes(digest[:16], "big") % 10**30).zfill(30)
    return SafetyNumber(
        numeric=_group_digits(number, 5),
        short_code="-".join(number[i : i + 3] for i in range(0, 12, 3)),
        fingerprint=b64e(digest),
    )
