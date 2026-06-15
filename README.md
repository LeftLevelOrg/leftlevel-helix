# LeftLevel Helix v0.2 Prototype

**LeftLevel Helix** is an experimental, original secure-messaging protocol prototype for the LeftLevel project: _Decentralized Privacy — Built to Stay Online_.

This repository demonstrates a two-person, invite-only, server-blind encrypted conversation flow. It uses open standards and vetted primitives rather than copying an app protocol or inventing new mathematics.

## What this prototype does

- No accounts, usernames, phone numbers, or emails.
- Invite-only pairing.
- Hybrid handshake:
  - X25519 classical ECDH.
  - ML-KEM-768 post-quantum KEM via OpenSSL 3.5+.
  - HKDF transcript-bound key derivation.
- Per-message symmetric ratchet.
- ChaCha20-Poly1305 authenticated encryption.
- Rotating mailbox IDs so the relay does not need conversation IDs or user IDs.
- Blind relay that stores only encrypted envelopes by mailbox ID.
- Fixed-block message padding for small messages.
- Tests for handshake, encryption, replay rejection, tamper rejection, and relay blindness.

## What this prototype does not yet do

- It is **not production-ready**.
- It has **not been independently audited**.
- v0.2 supports in-order delivery only.
- v0.2 supports two users only.
- v0.2 does not yet include mobile apps, out-of-order skipped-message keys, group MLS-style trees, mixnet routing, or hardened local secure storage.
- It cannot protect messages displayed on a fully compromised endpoint.

## Why this is not “stealing Signal”

This project does not copy Signal Protocol code or claim to be Signal-compatible. It uses public standards and common cryptographic building blocks:

- NIST ML-KEM-768 for post-quantum key encapsulation.
- X25519 for classical ECDH.
- HKDF for key derivation.
- ChaCha20-Poly1305 for AEAD.
- Ed25519 for pseudonymous self-signing of invite/response material.

The innovation target is the **LeftLevel architecture**: invite-only pseudonymous identity, server-blind rotating mailbox delivery, decentralizable relays, strict no-logs posture, secure-compose goals, and protocol-level metadata minimization.

## Requirements

- Python 3.11+
- OpenSSL 3.5+ with ML-KEM-768 support
- Python packages listed in `pyproject.toml`

Check OpenSSL support:

```bash
openssl version
openssl list -kem-algorithms | grep -i ML-KEM-768
```

## Run the demo

```bash
cd leftlevel-helix-v0.2
python examples/demo_two_users.py
```

Expected output:

```text
Bob received: Hello Bob. This is encrypted and relay-blind.
Alice received: Hi Alice. The server still cannot read this.
Relay audit snapshot after fetches: {}
```

## Run tests

```bash
cd leftlevel-helix-v0.2
pytest -q
```

## Run the prototype relay

```bash
uvicorn leftlevel_helix.relay:app --reload --port 8787
```

Endpoints:

- `POST /v0/envelopes`
- `GET /v0/envelopes/{mailbox_id}`
- `GET /v0/audit` for prototype inspection only

## Security status

This is a working research prototype. Treat it as a foundation for design review and iteration, not something to use for sensitive real-world messages yet.

See:

- `PROTOCOL.md`
- `SECURITY_MODEL.md`
- `ROADMAP.md`
