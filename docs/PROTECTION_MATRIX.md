# LeftLevel Helix Protection Matrix

This document explains what LeftLevel Helix is designed to protect, what it only reduces, and what remains outside the current prototype boundary.

## Current status

LeftLevel Helix v0.4 is a research prototype. It is not production-ready and has not been independently audited.

## Strong protections in the current design

| Area | What LeftLevel protects | How |
|---|---|---|
| Message content in transit | Network observers and the relay cannot read plaintext messages. | Messages are encrypted before they leave the sender using per-message keys and authenticated encryption. |
| Relay database compromise | A copied relay database should not contain plaintext message content. | The relay stores encrypted envelopes keyed by random-looking mailbox IDs. |
| Plaintext server access | The relay does not need user accounts, phone numbers, emails, contact names, or message bodies. | The relay API accepts mailbox IDs and ciphertext envelopes only. |
| Message tampering | Modified ciphertext or authenticated headers are rejected. | Authenticated encryption binds the header to the ciphertext. |
| Replay of consumed messages | Replaying the same consumed envelope is rejected. | Consumed mailbox IDs are tracked in session state. |
| Harvest-now-decrypt-later risk | Future quantum decryption risk is reduced. | The handshake combines X25519 with ML-KEM-768 when the OpenSSL provider is available. |
| First-contact tampering after verification | A swapped or mismatched invite/response is detectable. | Invite and response signatures are verified and bound into a safety number. |

## Protections that are reduced but not eliminated

| Area | Current posture | What must improve before production |
|---|---|---|
| Metadata leakage | Relay-visible metadata is minimized, but timing, IP address, message size class, and relay usage still exist. | Add relay rotation, optional privacy routing, cover traffic, and stricter TTLs. |
| Man-in-the-middle on first contact | Safety numbers reveal mismatched handshakes, but users still need a trusted comparison path. | Add assisted verification requests, QR verification, contact trust state, and change alerts. |
| Local device theft | Vault files are encrypted with a passphrase, but there is not yet a full secure local database or OS keychain integration. | Add mobile keystore/keychain support, app lock, secure storage, and encrypted message history. |
| Message size leakage | Small messages are padded to block boundaries, but large attachments and timing can still leak patterns. | Add attachment chunking, padding profiles, and background delivery queues. |
| Availability | Relays can be blocked or go offline. | Add multiple relays, relay failover, and offline/local transport options. |

## Not protected by cryptography alone

LeftLevel cannot fully protect against:

- malware on the user's device;
- a malicious keyboard, screen reader, or accessibility overlay;
- screenshots or camera photos of the screen;
- a recipient intentionally forwarding or copying a message;
- a compromised operating system;
- coercion or forced device unlock;
- global traffic analysis without stronger network privacy features;
- unverified first-contact impersonation.

## Production readiness gates

Before real sensitive use, LeftLevel needs:

1. Independent cryptographic review.
2. Formal threat model review.
3. Mobile secure storage review aligned to OWASP MASVS.
4. Reproducible builds.
5. Fuzz testing and static analysis.
6. External security assessment.
7. Clear user education around verification and endpoint limits.
