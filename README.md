# LeftLevel Helix v0.5 Prototype

**LeftLevel Helix** is an experimental, original secure-messaging protocol prototype for the LeftLevel project: _Decentralized Privacy — Built to Stay Online_.

This repository demonstrates a two-person, invite-only, server-blind encrypted conversation flow. It uses open standards and vetted primitives rather than copying an app protocol or inventing new mathematics.

> Package version: v0.5.0. Current wire protocol name: `LLH-HELIX-v0.2`.

## Current product focus

The near-term goal is simple: get a working product experience before adding Discord, Slack, browser, or mobile-share integrations.

v0.5 focuses on:

- pairing two people;
- verifying the contact;
- sending encrypted messages through a blind relay;
- receiving encrypted messages;
- keeping encrypted local contact and message history;
- showing clear trust labels.

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
- Encrypted local vault files for identities, invite drafts, and session state.
- Encrypted local app store for contacts, trust labels, sessions, and message history.
- Bounded out-of-order receive handling.
- HTTP relay client and CLI send/receive commands.
- Safety-number verification for invite/response handshakes.
- Tests for handshake, encryption, replay rejection, tamper rejection, out-of-order receive handling, encrypted vault persistence, relay blindness, HTTP relay client behavior, safety-number behavior, and local app-store messaging flow.

## What this prototype does not yet do

- It is **not production-ready**.
- It has **not been independently audited**.
- v0.5 supports two users only.
- v0.5 does not yet include mobile apps, group MLS-style trees, mixnet routing, hardened OS keychain/keystore integration, or a production database.
- It cannot protect messages displayed on a fully compromised endpoint.

## Man-in-the-middle posture

The invite and response are signed and transcript-bound, so tampering is detected once the expected invite/response pair is used. A relay or network cannot silently change the handshake without breaking verification.

However, no invite-only system can fully prevent a first-contact impersonation if users accept an invite through an untrusted channel and never compare verification codes. Safety-number verification lets both users compare the same short code out-of-band before trusting a contact.

```bash
leftlevel-verify --invite invite.llh.json --response response.llh.json
```

Both people should see the same safety number. If the numbers differ, do not trust that contact/session.

## Minimal local app workflow

The `leftlevel-app` command gives the prototype a simple product-shaped workflow with contacts, trust labels, and local message history stored inside an encrypted app vault.

```bash
leftlevel-app init
leftlevel-app add-contact bob --session alice-session.llh.vault
leftlevel-app contacts
leftlevel-app verify-contact bob
leftlevel-app send bob "hello" --relay-url http://127.0.0.1:8787
leftlevel-app receive bob --relay-url http://127.0.0.1:8787
leftlevel-app history bob
```

This is the recommended product path before adding Discord, Slack, browser, or mobile-share integrations.

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
- OpenSSL 3.5+ with ML-KEM-768 support for real post-quantum handshakes
- Python packages listed in `pyproject.toml`

Check OpenSSL support:

```bash
openssl version
openssl list -kem-algorithms | grep -i 'ML-KEM-768\|MLKEM768'
```

## Run the local demo

```bash
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
pytest -q
```

GitHub Actions runs the portable protocol suite as the required CI path and treats the real OpenSSL ML-KEM integration check as environment-dependent.

## Run the prototype relay

```bash
uvicorn leftlevel_helix.relay:app --reload --port 8787
```

Endpoints:

- `POST /v0/envelopes`
- `GET /v0/envelopes/{mailbox_id}`
- `GET /health`
- `GET /v0/audit` only when audit mode is enabled

## Security status

This is a working research prototype. Treat it as a foundation for design review and iteration, not something to use for sensitive real-world messages yet.

See:

- `PROTOCOL.md`
- `SECURITY_MODEL.md`
- `ROADMAP.md`
- `PRODUCTION_READINESS.md`
- `docs/WORKING_PRODUCT_PLAN.md`
- `docs/PROTECTION_MATRIX.md`
