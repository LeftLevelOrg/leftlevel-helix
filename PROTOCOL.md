# LeftLevel Helix Protocol v0.2

## Design goals

1. Make the server a blind relay, not a conversation participant.
2. Avoid account identifiers such as phone numbers and email addresses.
3. Use hybrid classical + post-quantum key establishment.
4. Give every message a fresh encryption key.
5. Rotate delivery mailboxes so the relay does not need to know the conversation graph.
6. Keep the protocol simple enough to test and explain.

## Non-goals in v0.2

- Production security claims.
- Large group messaging.
- Strong global traffic-analysis resistance.
- Mobile endpoint hardening.

## Actors

- Initiator: Alice.
- Responder: Bob.
- Relay: an untrusted message dropbox.

## Identity

Each user has an Ed25519 signing key. This key is not tied to a phone number, email, or server account. It is a pseudonymous contact identity.

The v0.2 invite is self-signed. This protects the invite from tampering but does not prove a real-world identity. Human verification or QR scanning provides trust-on-first-use.

## Handshake

Alice creates an invite containing:

- protocol version
- random conversation ID
- Alice pseudonymous signing public key
- Alice X25519 ephemeral public key
- Alice ML-KEM-768 public key
- Alice signature over the invite body

Bob accepts the invite and returns:

- protocol version
- same conversation ID
- Bob pseudonymous signing public key
- Bob X25519 ephemeral public key
- ML-KEM-768 ciphertext generated to Alice's ML-KEM public key
- hash of Alice's invite
- Bob signature over the response body

Both sides compute:

- `classical_secret = X25519(ephemeral_private, peer_ephemeral_public)`
- `pq_secret = ML-KEM-768 shared secret`
- `transcript_hash = SHA-256(canonical_json(invite, response))`
- `master = HKDF(classical_secret || pq_secret, salt=transcript_hash, info="hybrid-x25519-mlkem768-handshake-master")`

Then direction-specific chain keys and mailbox keys are derived from the master/root key.

## Message encryption

Each direction has a separate chain key. For every message:

1. Derive a one-time message key from the current chain key.
2. Derive a nonce from the current chain key.
3. Advance the chain key and delete the old value.
4. Derive the next mailbox ID from the direction mailbox key and counter.
5. Pad the plaintext to a fixed 256-byte block boundary.
6. Encrypt with ChaCha20-Poly1305 using authenticated header data.

## Relay-visible envelope

The relay sees only:

```json
{
  "mailbox_id": "random-looking value",
  "header": {
    "v": "LLH-HELIX-v0.2",
    "mailbox_id": "same random-looking value",
    "padding_block": 256,
    "direction": "i2r"
  },
  "ciphertext": "base64url ciphertext"
}
```

The relay does not need:

- sender ID
- recipient ID
- username
- conversation title
- group membership
- plaintext

## Replay and out-of-order handling

A consumed mailbox ID is remembered. Reusing the same envelope is rejected.

v0.2 includes a bounded skipped-message-key window. If a later mailbox arrives before an earlier mailbox, the receiver derives and caches skipped message keys up to the configured window. Messages outside that window are rejected without advancing state.

## Known v0.2 limitations

- The `direction` field is authenticated but visible. A future version should encrypt more header fields and keep only the mailbox visible to the relay.
- Out-of-order delivery is supported only within a bounded skipped-message-key window.
- No group tree or sender-key system yet.
- No periodic post-quantum rekey yet after the initial handshake.
- No local encrypted database yet.
