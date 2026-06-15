# App Architecture Decision

This document records the current product direction for LeftLevel Helix.

## Decision

Build a simple working product first, then evolve toward a modern cross-platform app.

Near term:

- keep the Python implementation as the reference protocol prototype;
- keep the CLI and encrypted app store working;
- build a small desktop playground UI around the existing product flow;
- avoid Discord, Slack, browser, and mobile-share integrations until the core app is stable.

Medium term:

- migrate the security-critical core into a Rust library;
- use a cross-platform app shell with a web UI and native system integration;
- preserve the same protocol test vectors and documentation.

## Recommended app stack

Recommended product stack: Tauri v2 + Rust core + web UI.

Reasons:

- one app shell can target Windows, macOS, Linux, Android, and iOS;
- Rust is a good fit for security-sensitive local code;
- web UI keeps product iteration fast;
- smaller app footprint than Electron-style packaging;
- native integrations can be added carefully over time.

## Current layers

```text
User interface
  -> leftlevel-app commands today
  -> desktop playground UI next
  -> Tauri app later

Product state
  -> encrypted app store
  -> contacts, trust labels, sessions, message history

Protocol core
  -> invite/response handshake
  -> hybrid X25519 plus ML-KEM-768
  -> message ratchet
  -> rotating mailboxes

Relay
  -> blind envelope store
  -> no accounts, no plaintext, no contact names
```

## Why not integrations first?

Integrations are useful, but they should not be the first product surface. The core product must work by itself first.

Future integrations should be limited to:

- discovery;
- invite launch;
- notification;
- onboarding;
- documentation links.

They should not receive plaintext secure messages.

## Recommended next milestone

Build a desktop playground UI that wraps the current v0.5 flow:

- create/open encrypted app store;
- list contacts;
- show trust badge;
- show local history;
- send through relay;
- receive from relay;
- rename contact;
- verify contact.

## Production migration path

1. Keep Python reference implementation and tests.
2. Add protocol test vectors.
3. Build a minimal desktop playground.
4. Port crypto/session/store core to Rust.
5. Use Tauri for desktop/mobile app shell.
6. Add OS keychain/keystore support.
7. Add signed builds and reproducible build process.
8. Add mobile MASVS review before public production claims.
