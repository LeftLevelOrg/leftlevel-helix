# UI Extraction Plan

This plan describes how the current desktop playground should become a dedicated application repository without weakening the protocol boundary.

## Current location

The current playground lives in:

```text
apps/desktop-playground
```

It remains in this repository while the local API and protocol contracts are still evolving.

## Target repository

The future app repository should be:

```text
LeftLevelOrg/leftlevel-app
```

That repository should become the home for the production desktop and mobile interface.

## Extraction prerequisites

Before moving the UI, the Helix repository should provide stable contracts for:

- local API health, contacts, history, verify, rename, send, and receive;
- message history response shape;
- trust state names;
- attachment integrity status names;
- relay URL configuration;
- local encrypted store setup;
- pairing and safety-number workflow.

## UI milestones before extraction

The playground should support the following before extraction:

1. Open or create an encrypted local store.
2. Pair or import a paired session.
3. Display contact trust state.
4. Display and compare safety numbers.
5. Send a non-sensitive test message through the local API.
6. Receive a non-sensitive test message through the local API.
7. Show delivery, empty, and failure states.
8. Show attachment integrity statuses from real data.

## App repository responsibilities

After extraction, `leftlevel-app` should own:

- Tauri or desktop shell configuration;
- app routing and screens;
- onboarding and setup UI;
- pairing and import UI;
- message and attachment views;
- build, packaging, and app release workflows;
- app-specific design assets.

## Helix repository responsibilities after extraction

After extraction, `leftlevel-helix` should continue to own:

- protocol behavior;
- cryptographic/session code;
- local API contract reference;
- reference relay behavior;
- security model and threat model;
- test vectors;
- compatibility and migration notes.

## Security rule

The app should call stable Helix interfaces instead of reimplementing protocol behavior. Protocol, storage, identity, safety-number, and attachment integrity behavior should stay reviewable in the core repository.
