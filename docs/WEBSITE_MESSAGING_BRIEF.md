# Website Messaging Brief

This brief provides public-facing language for future website updates. It should be kept aligned with the repository documentation and current implementation status.

## Core positioning

LeftLevel Helix is a security-first open-source messaging protocol and app prototype focused on protected conversations, fast delivery, and a user-friendly interface.

## Priority message

The primary message should be security first. Speed, usability, and extensibility matter, but they should be presented as supporting values that do not override the security model.

Suggested framing:

- Secure by design.
- Fast by engineering.
- Usable by default.
- Open for review.

## Short description

LeftLevel Helix is an open-source secure messaging prototype designed around pairwise identity, sealed message metadata, encrypted local storage, attachment integrity checks, and relay-facing metadata minimization.

## Longer description

LeftLevel Helix explores a local-first secure messaging architecture where contacts, sessions, and message history stay encrypted locally, relays handle opaque encrypted payloads, and users receive clear trust and integrity indicators in the interface.

The project is currently a prototype and reference implementation. It is not yet a production-ready or independently audited secure messenger.

## Messaging pillars

### Secure first

Security and privacy protection are the primary design goals. Protocol, storage, relay, attachment, and UI decisions should preserve or improve the security model.

### Fast messaging

The product should feel responsive through efficient local operations, bounded receive windows, retryable transfer units, and chunked handling for large payloads.

### User-friendly interface

The interface should make secure behavior understandable through trust labels, safety-number verification, attachment integrity states, and clear mitigation options.

### Open protocol and reviewability

The project should be transparent, testable, and documented so contributors and reviewers can evaluate the design.

## Current feature language

Use language such as:

- pairwise pseudonymous identity;
- sealed message metadata;
- encrypted local app store;
- server-blind relay direction;
- attachment integrity reports;
- opaque attachment transfer packages;
- review-ready reference implementation;
- modern desktop playground.

## Avoid overclaims

Do not describe the project as:

- production-ready;
- independently audited;
- metadata-free;
- anonymous by default;
- impossible to trace;
- a replacement for mature secure messengers.

## Suggested homepage sections

1. Hero: security-first messaging protocol and app prototype.
2. How it works: local encrypted storage, sealed messages, opaque relays.
3. Trust model: pairwise identity, safety numbers, changed-state warnings.
4. Attachments: encrypted chunks, integrity checks, blocked/warning states.
5. Open source: reviewable code, tests, documentation, roadmap.
6. Status: prototype, not audited, not production-ready.

## Website call to action

Recommended call to action:

- View the code.
- Review the protocol.
- Follow the roadmap.
- Contribute safely.
