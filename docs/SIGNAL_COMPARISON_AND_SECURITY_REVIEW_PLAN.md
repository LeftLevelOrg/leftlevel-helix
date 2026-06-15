# Signal Comparison and Security Review Plan

This document explains what LeftLevel can learn from Signal and what review work LeftLevel needs before production claims.

## How Signal works at a high level

Signal-style private messaging has three major layers:

1. An asynchronous key agreement so Alice can start a conversation even if Bob is offline.
2. A ratchet so every message uses a fresh key.
3. User verification so people can detect first-contact impersonation.

Signal's public specifications describe X3DH, PQXDH, and the Double Ratchet. LeftLevel is not copying those protocols, but we should learn from their maturity, documentation style, and review process.

## Signal-style lessons for LeftLevel

| Signal lesson | LeftLevel action |
|---|---|
| Publish clear protocol docs. | Keep `PROTOCOL.md`, `SECURITY_MODEL.md`, and protection docs current. |
| Use ratchets for message keys. | Keep per-message key rotation and bounded out-of-order handling. |
| Support asynchronous contact setup. | Keep invite/response flow simple before adding directories. |
| Make verification visible. | Keep safety numbers and trust badges clear. |
| Accept external review. | Plan independent review before production claims. |
| Avoid unsupported claims. | Never claim unhackable, metadata-free, or production-ready without review. |

## Do we need third-party testing?

Yes, but not at prototype stage before the product workflow works.

Before production or real sensitive use, LeftLevel should have:

1. Internal tests and CI.
2. Protocol test vectors.
3. Static analysis.
4. Dependency review.
5. Independent cryptographic review.
6. Mobile/desktop application security review.
7. Relay and deployment review.
8. Public security report or summary.

## What kind of sign-off matters?

A useful security sign-off is not just one test run. It should include:

- scope of review;
- commit or release reviewed;
- threat model;
- findings and severity;
- fixes applied;
- unresolved risks;
- explicit statement about what was not reviewed.

## Near-term review path

For now, LeftLevel should focus on:

1. Passing CI reliably.
2. Expanding tests around app-store behavior.
3. Adding protocol test vectors.
4. Keeping docs honest.
5. Creating a review-ready technical brief.

After the desktop playground works, commission or request expert review of:

- handshake design;
- ratchet state;
- local storage;
- safety-number verification;
- relay metadata;
- build/release pipeline.

## Important distinction

Signal is a mature, widely deployed project with years of public scrutiny and academic analysis. LeftLevel is a prototype. We can aim for that standard, but we should not claim that level of assurance until the project earns it.
