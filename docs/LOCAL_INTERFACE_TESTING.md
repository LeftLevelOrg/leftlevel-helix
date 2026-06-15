# Local Interface Testing

This guide explains how to view the current LeftLevel desktop playground and how to prepare for local interface testing.

## Current status

The interface is now more than a static mockup, but it is still a playground. It can show contacts, trust states, message history, composer behavior, attachment queue states, and attachment integrity states.

The interface can call the local API for message send and receive when a local app store, local API, and test relay are running.

It is not yet a packaged desktop app and should not be used for sensitive real-world messages.

## Mode 1: view the UI demo

This mode lets a tester see the interface without creating keys or a store.

```bash
python -m http.server 5173 --directory apps/desktop-playground
```

Then open:

```text
http://127.0.0.1:5173
```

Expected behavior:

- the UI opens in demo mode;
- the contact list appears;
- trust states are visible;
- attachment integrity states are visible;
- the composer supports long text and Unicode;
- send adds a local demo message only.

## Mode 2: local API interface testing

This mode is for developer testing with a local encrypted app store.

Start a test relay:

```bash
uvicorn leftlevel_helix.relay:app --reload --port 8787
```

Start the local API:

```bash
LLH_APP_STORE=leftlevel-app.llh.vault \
LLH_VAULT_PASSPHRASE='change-me' \
python -m leftlevel_helix.local_api
```

Serve the playground:

```bash
python -m http.server 5173 --directory apps/desktop-playground
```

Then open:

```text
http://127.0.0.1:5173
```

Expected behavior when the app store already contains contacts:

- the playground reads contacts from the local API;
- message history comes from the encrypted local app store;
- Send uses the local API message endpoint;
- Receive uses the local API message endpoint;
- the relay still handles encrypted envelopes only.

## Important setup note

The local API requires an existing encrypted app store with contacts and sessions. Creating that store is currently a CLI workflow. A future interface milestone should add UI-based pairing and contact setup.

## Friend testing readiness

Do not ask a non-developer friend to test the full workflow yet. The interface still needs:

- UI-based encrypted store creation;
- UI-based pairing;
- UI-based safety-number comparison;
- clearer setup guidance;
- packaged app startup;
- real attachment transfer through the UI.

For now, friend testing should wait until the setup is simpler and the interface can create or import the needed local state without CLI steps.

## Security guidance

Use harmless test messages and sample files only. Do not use sensitive real-world messages while the project remains a prototype and review candidate.
