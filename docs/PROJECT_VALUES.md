# Project Values

LeftLevel Helix is guided by a security-first product philosophy. Features, performance work, protocol changes, UI changes, and documentation should reinforce that priority.

## Priority order

1. Security and privacy protection.
2. Correctness and reviewability.
3. Fast and reliable messaging.
4. User-friendly interface design.
5. Extensibility for future clients, relays, and integrations.

## Security first

Security is the primary project value. A feature should not be added if it weakens message confidentiality, identity safety, local storage protection, or attachment integrity without a clear review path and documented tradeoff.

Security work includes:

- encrypted message content;
- sealed message metadata where practical;
- pairwise pseudonymous identity;
- local encrypted storage;
- explicit trust and safety-number verification;
- attachment integrity verification;
- relay-facing minimization of plaintext and metadata;
- conservative public claims until review is complete.

## Correctness and reviewability

The project should be easy to inspect, test, and port. Protocol behavior should be documented and covered by tests before it becomes part of the product experience.

Implementation work should favor:

- small, testable modules;
- clear serialization formats;
- deterministic fixtures where appropriate;
- explicit threat-model notes;
- honest limitations;
- review-ready documentation.

## Fast and reliable messaging

The protocol and app should feel responsive while preserving security boundaries.

Performance work should focus on:

- efficient local storage access;
- bounded receive windows;
- chunked large payloads;
- retryable transfer units;
- relay operations that do not require plaintext inspection;
- responsive UI behavior under long messages and attachments.

Performance should not override the security model.

## User-friendly interface

The interface should make secure behavior understandable. Users should not need to understand cryptography to recognize verified contacts, changed safety state, blocked attachments, or resend options.

The UI should clearly communicate:

- verified, new, and changed contact states;
- attachment verification results;
- warnings and blocked states;
- clear mitigation options;
- what is local-only, queued, sent, received, or failed.

## Extensibility

The project should remain extensible for future desktop, mobile, web, relay, and self-hosted deployments.

Extensibility should be built around stable boundaries:

- reference protocol modules;
- local app APIs;
- relay-facing opaque payloads;
- portable test vectors;
- UI components that do not depend on plaintext relay access.

## Public positioning

Public materials should position LeftLevel Helix as a security-first, open-source messaging protocol and app prototype with a usability-focused product direction.

Until independent review is complete, public language should avoid claims that the project is production-ready, audited, anonymous by default, metadata-free, or impossible to trace.
