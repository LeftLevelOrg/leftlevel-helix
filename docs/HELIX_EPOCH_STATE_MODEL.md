# Helix Epoch State Model

This document proposes the next LeftLevel protocol direction after the current v0.5 prototype.

## Goal

Move from a simple message chain to a clearer conversation model with epochs.

An epoch is a period of a conversation that has its own local state:

- epoch number;
- send chain state;
- receive chain state;
- mailbox derivation state;
- trust metadata;
- local history markers.

## Why epochs help

Epochs make the protocol easier to reason about because important changes happen at named boundaries.

They can support:

- cleaner long-running conversations;
- future rekey events;
- better local state recovery checks;
- clearer safety-number continuity;
- more reviewable documentation;
- better UI warnings when contact state changes.

## Current prototype

The current prototype already has:

- invite and response pairing;
- transcript-bound session setup;
- independent send and receive chains;
- per-message keys;
- rotating mailbox IDs;
- bounded out-of-order receive handling;
- encrypted local app store.

The next model keeps that work and adds an explicit epoch layer.

## Proposed flow

```text
pair contact
  -> create epoch 0
  -> send and receive messages
  -> periodically create next epoch
  -> preserve contact trust continuity
```

Each message belongs to exactly one epoch.

The relay should not need to understand epochs. Epoch details belong inside the encrypted session state and encrypted message body.

## Header-minimization target

Over time, the relay-visible envelope should move toward:

```text
mailbox_id
ciphertext_length_class
ciphertext
```

Protocol version, counter, direction, epoch number, and message type should move inside encrypted content where practical.

## Privacy direction

LeftLevel should be careful with language. Encryption protects content, but network activity can still reveal patterns.

The staged privacy direction is:

1. Server-blind content handling.
2. Rotating mailbox delivery.
3. Smaller relay-visible headers.
4. Relay choice and relay rotation.
5. Optional advanced delivery modes for higher-risk users.

## Implementation plan

1. Add `epoch` to session state.
2. Add internal encrypted message types.
3. Add a state-refresh message type.
4. Add tests for epoch transitions.
5. Add protocol test vectors.
6. Update the protection matrix.
7. Seek expert review before production claims.

## Product UI impact

The UI should stay simple:

- OK means trusted contact state is current.
- NEW means not verified yet.
- CHANGED means identity or state continuity changed and the user should verify again.

The user should not need to understand epochs in normal use.

## Project rule

Use well-reviewed primitives. Make LeftLevel original through product design, relay minimization, contact model, state model, and usability.
