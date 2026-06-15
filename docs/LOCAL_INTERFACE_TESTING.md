# Local Interface Testing

This guide explains how to view the current LeftLevel desktop playground and how to prepare for local interface testing.

## Current status

The interface is now more than a static mockup, but it is still a playground. It can show contacts, trust states, message history, local setup status, Add friend actions, composer behavior, attachment queue states, and attachment integrity states.

The interface can call the local API for encrypted store creation, setup readiness, prototype Add friend actions, message send, and message receive when the local API and test relay are running.

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
- the local setup panel shows that the local API is not connected;
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

Expected behavior:

- the playground detects the local API;
- Open encrypted store creates the configured local vault if it is missing;
- the local setup panel shows store readiness and contact count;
- message history comes from the encrypted local app store after contacts exist;
- Send uses the local API message endpoint;
- Receive uses the local API message endpoint;
- the relay still handles encrypted envelopes only.

## Open encrypted store

The Open encrypted store button calls the local API setup create endpoint.

The browser does not receive the vault passphrase. The local API uses the configured `LLH_VAULT_PASSPHRASE` and `LLH_APP_STORE` values.

Expected statuses:

- `created`: the encrypted store was created;
- `already_exists`: the encrypted store already exists;
- failure message: the local API could not create or open the configured store.

## Prototype Add friend panel

The Add friend panel can call local API prototype actions:

- Create friend invite: creates a local invite and pending encrypted draft, then prints JSON for copy/paste testing;
- Accept friend invite: asks for a local contact name and pasted invite JSON, then saves a contact and prints response JSON;
- Finish adding friend: asks for a draft ID, local contact name, and pasted response JSON, then saves the paired contact.

This is a prototype copy/paste flow. A future interface should replace prompts with guided screens and file import/export.

## Setup states

The local setup panel may show:

- `ready`: encrypted store exists and at least one contact is available;
- `empty_store`: encrypted store exists but no contacts are available;
- `missing_store`: the local API is running but the configured store file is missing;
- demo mode: the local API is not connected.

## Important setup note

The local API can now create the configured encrypted app store. Contact setup can be exercised through prototype Add friend actions, but the UI still needs a guided, polished setup flow before non-developer friend testing.

## Friend testing readiness

Do not ask a non-developer friend to test the full workflow yet. The interface still needs:

- guided Add friend screens instead of prompt dialogs;
- UI-based safety-number comparison;
- clearer setup guidance;
- packaged app startup;
- real attachment transfer through the UI.

For now, friend testing should wait until the setup is simpler and the interface can create or import the needed local state without manual JSON copy/paste.

## Security guidance

Use harmless test messages and sample files only. Do not use sensitive real-world messages while the project remains a prototype and review candidate.
