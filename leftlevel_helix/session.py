from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption

from .identity import Identity, verify_signature
from .kem import MlKem768PrivateKey, mlkem768_encapsulate
from .primitives import aead_decrypt, aead_encrypt, advance_chain, hkdf, random_bytes, sha256
from .util import b64d, b64e, canonical_json

PROTOCOL_NAME = "LLH-HELIX-v0.2"
DEFAULT_SKIP_WINDOW = 64


def _x25519_pub(priv: X25519PrivateKey) -> bytes:
    return priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)


def _x25519_priv_bytes(priv: X25519PrivateKey) -> bytes:
    return priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())


def _x25519_exchange(priv: X25519PrivateKey, peer_public_raw: bytes) -> bytes:
    return priv.exchange(X25519PublicKey.from_public_bytes(peer_public_raw))


def _pad(plaintext: bytes, block_size: int = 256) -> bytes:
    if len(plaintext) > 16_777_215:
        raise ValueError("message too large for v0.2 padding")
    if block_size < 64 or block_size > 4096:
        raise ValueError("unsupported padding block size")
    prefix = len(plaintext).to_bytes(3, "big")
    payload = prefix + plaintext
    pad_len = (-len(payload)) % block_size
    return payload + os.urandom(pad_len)


def _unpad(padded: bytes) -> bytes:
    if len(padded) < 3:
        raise ValueError("invalid padded plaintext")
    size = int.from_bytes(padded[:3], "big")
    if size > len(padded) - 3:
        raise ValueError("invalid padding length")
    return padded[3 : 3 + size]


@dataclass
class HelixInvite:
    body: dict[str, Any]
    signature: str

    def to_dict(self) -> dict[str, Any]:
        return {"body": self.body, "signature": self.signature}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HelixInvite":
        return cls(body=data["body"], signature=data["signature"])

    def verify_self_signature(self) -> None:
        verify_signature(
            b64d(self.body["alice_identity_pub"]),
            canonical_json(self.body),
            b64d(self.signature),
        )


@dataclass
class HelixResponse:
    body: dict[str, Any]
    signature: str

    def to_dict(self) -> dict[str, Any]:
        return {"body": self.body, "signature": self.signature}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HelixResponse":
        return cls(body=data["body"], signature=data["signature"])

    def verify_self_signature(self) -> None:
        verify_signature(
            b64d(self.body["bob_identity_pub"]),
            canonical_json(self.body),
            b64d(self.signature),
        )


@dataclass
class AliceDraft:
    identity: Identity
    x25519_private: X25519PrivateKey
    mlkem_private: MlKem768PrivateKey
    invite: HelixInvite

    def to_state_dict(self) -> dict[str, Any]:
        """Export the sensitive draft state.

        This is required so a non-technical client can create an invite, close the
        app, and later finalize the response. Store this only inside the encrypted
        vault in production clients.
        """
        return {
            "v": PROTOCOL_NAME,
            "identity_private": self.identity.export_private_b64(),
            "x25519_private": b64e(_x25519_priv_bytes(self.x25519_private)),
            "mlkem768_private_pem": b64e(self.mlkem_private.private_pem),
            "invite": self.invite.to_dict(),
        }

    @classmethod
    def from_state_dict(cls, data: dict[str, Any]) -> "AliceDraft":
        if data.get("v") != PROTOCOL_NAME:
            raise ValueError("unsupported draft version")
        return cls(
            identity=Identity.import_private_b64(data["identity_private"]),
            x25519_private=X25519PrivateKey.from_private_bytes(b64d(data["x25519_private"])),
            mlkem_private=MlKem768PrivateKey(b64d(data["mlkem768_private_pem"])),
            invite=HelixInvite.from_dict(data["invite"]),
        )


@dataclass
class Envelope:
    mailbox_id: str
    header: dict[str, Any]
    ciphertext: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "mailbox_id": self.mailbox_id,
            "header": self.header,
            "ciphertext": self.ciphertext,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Envelope":
        return cls(
            mailbox_id=data["mailbox_id"],
            header=data["header"],
            ciphertext=data["ciphertext"],
        )


@dataclass
class SkippedMessageKey:
    counter: int
    message_key: bytes
    nonce: bytes

    def to_state_dict(self) -> dict[str, Any]:
        return {"counter": self.counter, "message_key": b64e(self.message_key), "nonce": b64e(self.nonce)}

    @classmethod
    def from_state_dict(cls, data: dict[str, Any]) -> "SkippedMessageKey":
        return cls(counter=int(data["counter"]), message_key=b64d(data["message_key"]), nonce=b64d(data["nonce"]))


@dataclass
class HelixSession:
    conversation_id: str
    role: str  # "initiator" or "responder"
    root_key: bytes
    send_chain_key: bytes
    recv_chain_key: bytes
    send_mailbox_key: bytes
    recv_mailbox_key: bytes
    alice_identity_pub: bytes
    bob_identity_pub: bytes
    transcript_hash: bytes
    send_counter: int = 0
    recv_counter: int = 0
    seen_mailboxes: set[str] = field(default_factory=set)
    skipped_message_keys: dict[str, SkippedMessageKey] = field(default_factory=dict)
    max_skip: int = DEFAULT_SKIP_WINDOW

    def _mailbox_id(self, key: bytes, counter: int) -> str:
        raw = sha256(key + counter.to_bytes(8, "big") + b"|mailbox")[:20]
        return b64e(raw)

    def next_receive_mailbox(self) -> str:
        return self._mailbox_id(self.recv_mailbox_key, self.recv_counter + 1)

    def safety_number(self):
        from .verification import session_safety_number

        return session_safety_number(
            protocol_name=PROTOCOL_NAME,
            conversation_id=self.conversation_id,
            alice_identity_pub=self.alice_identity_pub,
            bob_identity_pub=self.bob_identity_pub,
            transcript_hash=self.transcript_hash,
        )

    def peer_identity_fingerprint(self) -> str:
        peer_key = self.bob_identity_pub if self.role == "initiator" else self.alice_identity_pub
        return b64e(sha256(b"LLH-PEER-IDENTITY-v1|" + peer_key))

    def seal(self, plaintext: bytes, *, padding_block: int = 256) -> Envelope:
        counter = self.send_counter + 1
        mailbox_id = self._mailbox_id(self.send_mailbox_key, counter)
        step = advance_chain(self.send_chain_key)
        header = {
            "v": PROTOCOL_NAME,
            "mailbox_id": mailbox_id,
            "padding_block": padding_block,
            "direction": "i2r" if self.role == "initiator" else "r2i",
        }
        aad = canonical_json(header)
        ciphertext = aead_encrypt(step.message_key, step.nonce, _pad(plaintext, padding_block), aad)
        self.send_chain_key = step.next_chain_key
        self.send_counter = counter
        return Envelope(mailbox_id=mailbox_id, header=header, ciphertext=b64e(ciphertext))

    def open(self, envelope: Envelope) -> bytes:
        self._validate_envelope_header(envelope)
        if envelope.mailbox_id in self.seen_mailboxes:
            raise ValueError("replay detected: mailbox was already consumed")

        skipped = self.skipped_message_keys.pop(envelope.mailbox_id, None)
        if skipped is not None:
            plaintext = self._decrypt_with(envelope, skipped.message_key, skipped.nonce)
            self.seen_mailboxes.add(envelope.mailbox_id)
            return plaintext

        candidates: list[tuple[str, SkippedMessageKey]] = []
        scan_chain = self.recv_chain_key

        for counter in range(self.recv_counter + 1, self.recv_counter + self.max_skip + 2):
            mailbox = self._mailbox_id(self.recv_mailbox_key, counter)
            step = advance_chain(scan_chain)
            key_record = SkippedMessageKey(counter=counter, message_key=step.message_key, nonce=step.nonce)

            if mailbox == envelope.mailbox_id:
                plaintext = self._decrypt_with(envelope, key_record.message_key, key_record.nonce)
                for skipped_mailbox, skipped_key in candidates:
                    self.skipped_message_keys[skipped_mailbox] = skipped_key
                self.recv_chain_key = step.next_chain_key
                self.recv_counter = counter
                self.seen_mailboxes.add(envelope.mailbox_id)
                self._trim_replay_state()
                return plaintext

            candidates.append((mailbox, key_record))
            scan_chain = step.next_chain_key

        raise ValueError("unexpected mailbox: message is outside the receive skip window")

    def _validate_envelope_header(self, envelope: Envelope) -> None:
        if envelope.header.get("v") != PROTOCOL_NAME:
            raise ValueError("unsupported protocol version")
        if envelope.header.get("mailbox_id") != envelope.mailbox_id:
            raise ValueError("header/mailbox mismatch")
        expected_direction = "i2r" if self.role == "responder" else "r2i"
        if envelope.header.get("direction") != expected_direction:
            raise ValueError("wrong direction for this session")
        if envelope.header.get("padding_block") not in (64, 128, 256, 512, 1024, 2048, 4096):
            raise ValueError("unsupported padding block")

    def _decrypt_with(self, envelope: Envelope, message_key: bytes, nonce: bytes) -> bytes:
        aad = canonical_json(envelope.header)
        padded = aead_decrypt(message_key, nonce, b64d(envelope.ciphertext), aad)
        return _unpad(padded)

    def _trim_replay_state(self) -> None:
        if len(self.seen_mailboxes) > 4096:
            self.seen_mailboxes = set(list(self.seen_mailboxes)[-2048:])
        if len(self.skipped_message_keys) > self.max_skip:
            oldest = sorted(self.skipped_message_keys.items(), key=lambda item: item[1].counter)
            self.skipped_message_keys = dict(oldest[-self.max_skip :])

    def to_state_dict(self) -> dict[str, Any]:
        return {
            "v": PROTOCOL_NAME,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "root_key": b64e(self.root_key),
            "send_chain_key": b64e(self.send_chain_key),
            "recv_chain_key": b64e(self.recv_chain_key),
            "send_mailbox_key": b64e(self.send_mailbox_key),
            "recv_mailbox_key": b64e(self.recv_mailbox_key),
            "alice_identity_pub": b64e(self.alice_identity_pub),
            "bob_identity_pub": b64e(self.bob_identity_pub),
            "transcript_hash": b64e(self.transcript_hash),
            "send_counter": self.send_counter,
            "recv_counter": self.recv_counter,
            "seen_mailboxes": sorted(self.seen_mailboxes),
            "skipped_message_keys": {k: v.to_state_dict() for k, v in self.skipped_message_keys.items()},
            "max_skip": self.max_skip,
        }

    @classmethod
    def from_state_dict(cls, data: dict[str, Any]) -> "HelixSession":
        if data.get("v") != PROTOCOL_NAME:
            raise ValueError("unsupported session version")
        return cls(
            conversation_id=data["conversation_id"],
            role=data["role"],
            root_key=b64d(data["root_key"]),
            send_chain_key=b64d(data["send_chain_key"]),
            recv_chain_key=b64d(data["recv_chain_key"]),
            send_mailbox_key=b64d(data["send_mailbox_key"]),
            recv_mailbox_key=b64d(data["recv_mailbox_key"]),
            alice_identity_pub=b64d(data.get("alice_identity_pub", "")) if data.get("alice_identity_pub") else b"",
            bob_identity_pub=b64d(data.get("bob_identity_pub", "")) if data.get("bob_identity_pub") else b"",
            transcript_hash=b64d(data.get("transcript_hash", "")) if data.get("transcript_hash") else b"",
            send_counter=int(data["send_counter"]),
            recv_counter=int(data["recv_counter"]),
            seen_mailboxes=set(data.get("seen_mailboxes", [])),
            skipped_message_keys={k: SkippedMessageKey.from_state_dict(v) for k, v in data.get("skipped_message_keys", {}).items()},
            max_skip=int(data.get("max_skip", DEFAULT_SKIP_WINDOW)),
        )


def create_invite(identity: Identity) -> AliceDraft:
    xpriv = X25519PrivateKey.generate()
    mlkem = MlKem768PrivateKey.generate()
    body = {
        "v": PROTOCOL_NAME,
        "conversation_id": b64e(random_bytes(24)),
        "alice_identity_pub": b64e(identity.public_key_bytes()),
        "alice_x25519_pub": b64e(_x25519_pub(xpriv)),
        "alice_mlkem768_pub_pem": b64e(mlkem.public_pem()),
        "identity_model": "invite-only-pseudonymous",
        "capabilities": ["hybrid-x25519-mlkem768", "out-of-order-window-64", "rotating-mailboxes"],
    }
    sig = identity.sign(canonical_json(body))
    invite = HelixInvite(body=body, signature=b64e(sig))
    return AliceDraft(identity=identity, x25519_private=xpriv, mlkem_private=mlkem, invite=invite)


def accept_invite(identity: Identity, invite: HelixInvite) -> tuple[HelixResponse, HelixSession]:
    invite.verify_self_signature()
    if invite.body.get("v") != PROTOCOL_NAME:
        raise ValueError("unsupported invite version")

    bx = X25519PrivateKey.generate()
    classical = _x25519_exchange(bx, b64d(invite.body["alice_x25519_pub"]))
    kem_ct, pq_secret = mlkem768_encapsulate(b64d(invite.body["alice_mlkem768_pub_pem"]))

    body = {
        "v": PROTOCOL_NAME,
        "conversation_id": invite.body["conversation_id"],
        "bob_identity_pub": b64e(identity.public_key_bytes()),
        "bob_x25519_pub": b64e(_x25519_pub(bx)),
        "mlkem768_ciphertext": b64e(kem_ct),
        "invite_hash": b64e(sha256(canonical_json(invite.to_dict()))),
        "capabilities": ["hybrid-x25519-mlkem768", "out-of-order-window-64", "rotating-mailboxes"],
    }
    sig = identity.sign(canonical_json(body))
    response = HelixResponse(body=body, signature=b64e(sig))
    session = _derive_session(invite, response, classical, pq_secret, role="responder")
    return response, session


def finalize_invite(draft: AliceDraft, response: HelixResponse) -> HelixSession:
    draft.invite.verify_self_signature()
    response.verify_self_signature()
    if response.body.get("conversation_id") != draft.invite.body["conversation_id"]:
        raise ValueError("response is for a different conversation")
    expected_invite_hash = b64e(sha256(canonical_json(draft.invite.to_dict())))
    if response.body.get("invite_hash") != expected_invite_hash:
        raise ValueError("response did not bind to this invite")

    classical = _x25519_exchange(draft.x25519_private, b64d(response.body["bob_x25519_pub"]))
    pq_secret = draft.mlkem_private.decapsulate(b64d(response.body["mlkem768_ciphertext"]))
    return _derive_session(draft.invite, response, classical, pq_secret, role="initiator")


def _derive_session(
    invite: HelixInvite,
    response: HelixResponse,
    classical_secret: bytes,
    pq_secret: bytes,
    *,
    role: str,
) -> HelixSession:
    transcript = canonical_json({"invite": invite.to_dict(), "response": response.to_dict()})
    transcript_hash = sha256(transcript)
    master = hkdf(
        classical_secret + pq_secret,
        salt=transcript_hash,
        info=b"hybrid-x25519-mlkem768-handshake-master",
    )
    root = hkdf(master, salt=transcript_hash, info=b"root")
    i2r_chain = hkdf(root, salt=transcript_hash, info=b"chain:initiator-to-responder")
    r2i_chain = hkdf(root, salt=transcript_hash, info=b"chain:responder-to-initiator")
    i2r_mailbox = hkdf(root, salt=transcript_hash, info=b"mailbox:initiator-to-responder")
    r2i_mailbox = hkdf(root, salt=transcript_hash, info=b"mailbox:responder-to-initiator")

    if role == "initiator":
        send_chain, recv_chain = i2r_chain, r2i_chain
        send_box, recv_box = i2r_mailbox, r2i_mailbox
    elif role == "responder":
        send_chain, recv_chain = r2i_chain, i2r_chain
        send_box, recv_box = r2i_mailbox, i2r_mailbox
    else:
        raise ValueError("role must be initiator or responder")

    return HelixSession(
        conversation_id=invite.body["conversation_id"],
        role=role,
        root_key=root,
        send_chain_key=send_chain,
        recv_chain_key=recv_chain,
        send_mailbox_key=send_box,
        recv_mailbox_key=recv_box,
        alice_identity_pub=b64d(invite.body["alice_identity_pub"]),
        bob_identity_pub=b64d(response.body["bob_identity_pub"]),
        transcript_hash=transcript_hash,
    )
