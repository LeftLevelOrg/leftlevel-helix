# Roadmap

## v0.2 - Prototype foundation

- [x] Two-person invite handshake.
- [x] X25519 + ML-KEM-768 hybrid shared secret.
- [x] HKDF transcript binding.
- [x] Per-message symmetric ratchet.
- [x] Blind relay envelope store.
- [x] Replay/tamper tests.
- [x] Demo conversation.

## v0.2 - Usability and durability

- [x] Export/import complete session state through encrypted vault files.
- [ ] Encrypted local database.
- [ ] Desktop UI prototype.
- [ ] Relay HTTP client.
- [ ] Better error handling.
- [x] Out-of-order message receive window.

## v0.3 - Security hardening

- [ ] Header encryption so only mailbox ID is relay-visible.
- [ ] Periodic hybrid post-quantum rekey messages.
- [ ] Key transparency / safety number UX.
- [ ] Secure compose mode.
- [ ] CI fuzzing.
- [ ] Static analysis.

## v0.4 - Decentralization

- [ ] Multiple relay support.
- [ ] Relay rotation.
- [ ] Anonymous relay tokens or proof-of-work spam control.
- [ ] Optional Tor/I2P routing profile.

## v0.5 - Small groups

- [ ] Small invite-only groups.
- [ ] Member removal and group key rotation.
- [ ] Group transcript authentication.

## v1.0 readiness gates

- [ ] Independent cryptographic review.
- [ ] Formal threat model review.
- [ ] Reproducible builds.
- [ ] Mobile endpoint hardening.
- [ ] External penetration test.
