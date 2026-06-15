# Dependency Inventory

This document records the current direct dependencies and why they are used.

## Runtime dependencies

### `cryptography>=41`

Purpose:

- ChaCha20-Poly1305 authenticated encryption;
- HKDF key derivation;
- hash primitives;
- asymmetric primitive support used by the reference implementation.

Review notes:

- Security-sensitive dependency.
- Must be monitored for security updates.
- Production readiness should require pinned versions and dependency provenance review.

### `fastapi>=0.100`

Purpose:

- reference relay API;
- local UI API.

Review notes:

- Network-facing dependency when used for relay or local API.
- Production relay use should include deployment hardening, CORS review, and logging policy review.

### `uvicorn>=0.20`

Purpose:

- development and reference ASGI server for relay and local API.

Review notes:

- Production deployment may require a hardened process manager, service configuration, and monitoring.

## Development dependencies

### `pytest>=7`

Purpose:

- unit tests;
- integration-style reference tests;
- documentation guardrail tests.

## Build dependencies

### `setuptools>=68`

Purpose:

- package build backend.

### `wheel`

Purpose:

- wheel artifact creation.

## External runtime expectations

### Python 3.11+

The project currently requires Python 3.11 or newer.

### OpenSSL 3.5+ for real ML-KEM testing

The real ML-KEM integration path depends on OpenSSL support for ML-KEM-768. Portable CI may skip real-provider tests when the environment does not provide it.

## Production readiness requirements

Before production approval, dependency review should include:

- pinned dependency versions;
- dependency vulnerability scan;
- license review;
- build provenance review;
- release artifact reproducibility plan;
- upgrade and rollback process.
