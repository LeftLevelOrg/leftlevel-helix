# Helix Ratchet and Anonymity Model

This document clarifies the relationship between LeftLevel Helix and Signal-style ratchets, and defines the direction for stronger privacy/anonymity.

## We are not implementing Signal's Double Ratchet as-is

LeftLevel Helix currently uses a per-message symmetric ratchet after a hybrid invite handshake. That is not the same thing as Signal's full Double Ratchet.

A full Double Ratchet combines:

- a symmetric-key ratchet for every message;
- a Diffie-Hellman ratchet that periodically refreshes chain keys when new ratchet public keys arrive.

LeftLevel's current prototype has:

- hybrid X25519 plus ML-KEM-768 invite handshake;
- transcript-bound key derivation;
- independent send and receive chains;
- per-message message keys;
- rotating mailbox IDs;
- bounded out-of-order receive handling.

This makes LeftLevel simpler than Signal's full Double Ratchet today. It also means we should not claim Signal-equivalent security until we add stronger rekey and review.

## Originality position

LeftLevel should not claim to invent ratcheting or post-quantum cryptography.

The original contribution should be the product/protocol architecture:

- no required phone number, email, or central account identity;
- pairwise pseudonymous identity;
- server-blind rotating mailbox delivery;
- encrypted local app store;
- visible trust labels;
- safety-number verification;
- future relay rotation and optional privacy routing;
- clear protection documentation.

The project should use vetted cryptographic primitives and original glue/protocol architecture.

## Helix Ratchet direction

A future Helix ratchet should be documented as its own design and reviewed before production.

Recommended path:

1. Keep the current symmetric message ratchet stable.
2. Add periodic hybrid rekey messages.
3. Add header encryption so only mailbox ID remains relay-visible.
4. Add optional post-quantum rekey epochs.
5. Add protocol test vectors.
6. Submit the design for independent review.

## Anonymity model

Message encryption is not anonymity.

LeftLevel currently protects message content and reduces relay-visible metadata, but it does not fully hide:

- IP address from the relay;
- message timing;
- approximate message size class;
- whether a client is checking a relay;
- endpoint device behavior.

## Privacy goals by stage

### Stage 1: Server-blind content privacy

The relay should not see plaintext, contact names, accounts, or conversation names.

### Stage 2: Unlinkable mailbox delivery

Each message should use a fresh mailbox ID so the relay does not need a stable conversation ID.

### Stage 3: Header minimization

Headers should be encrypted or minimized so the relay sees only the mailbox ID and ciphertext.

### Stage 4: Network privacy options

Users should be able to use relay rotation, self-hosted relays, and optional privacy networks where appropriate.

### Stage 5: Traffic-analysis resistance

Advanced deployments may add batching, cover traffic, padding profiles, and delayed delivery. These improve privacy but increase cost and complexity.

## What to avoid claiming

Do not claim:

- fully anonymous;
- metadata-free;
- impossible to trace;
- Signal-equivalent;
- production-ready;
- secure against compromised endpoints.

Use narrower language:

- server-blind;
- accountless;
- pairwise pseudonymous;
- metadata-minimizing;
- post-quantum-ready direction;
- review-ready prototype.
