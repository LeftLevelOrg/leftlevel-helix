# Friend Testing Readiness

This document tracks what must be true before non-developer friend testing is appropriate.

## Current status

The desktop playground now shows the intended product direction: contacts, safety states, a composer, queued attachments, and attachment integrity states.

It is still a playground. It is not yet a packaged app and does not yet provide a complete friend-to-friend workflow through the interface.

## Ready now

A developer can currently test:

- protocol handshakes through the CLI;
- relay-backed encrypted text messages through the CLI;
- local app-store contacts and message history;
- desktop playground layout and UI states;
- attachment package encryption and integrity logic through tests;
- verified, warning, and blocked attachment states in the playground demo UI.

## Not ready yet

Friend testing should wait until the interface supports:

- creating or opening an encrypted local app store;
- pairing with another person from the UI;
- comparing a safety number from the UI;
- sending through the local API;
- receiving through the local API;
- showing message delivery and failure states;
- showing attachment verification and mitigation actions from real received data.

## Security-first testing rule

Testing should avoid sensitive real-world messages until the workflow is reviewed and the project is explicitly marked ready for broader trials.

Use harmless test messages and sample files only.

## Next milestone

The next milestone is a local interface test build where two people can:

1. start a local relay or use a test relay;
2. create local encrypted stores;
3. pair with invite and response files;
4. verify matching safety numbers;
5. send and receive non-sensitive test messages;
6. see attachment integrity states and mitigation options.
