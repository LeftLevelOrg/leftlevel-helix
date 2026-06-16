# Local Interface Testing

This guide explains how to view the current LeftLevel desktop playground and how to prepare for local interface testing.

## Current status

The interface is now more than a static mockup, but it is still a playground. It can show contacts, trust states, message history, local setup status, Add friend actions, composer behavior, attachment queue states, attachment integrity states, and link safety guidance.

The interface can call the local API for encrypted store creation, setup readiness, local link inspection, one-click test friend creation, one-click local test message delivery, prototype Add friend actions, message send, and message receive when the local API and test relay are running.

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
- link safety guidance is visible;
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
- Inspect links analyzes message text without opening URLs;
- Create test friend creates a verified local test pair for development;
- Send test message delivers a local encrypted loopback message between the test pair;
- the local setup panel shows store readiness and contact count;
- message history comes from the encrypted local app store after contacts exist;
- Send uses the local API message endpoint;
- Receive uses the local API message endpoint;
- the relay still handles encrypted envelopes only.

## Link inspection

The Inspect links button calls the local API link inspection endpoint.

Local link inspection does not fetch the website and does not open the URL. It parses the text and can flag obvious risks such as blocked schemes, localhost or private-network targets, plain HTTP, user-info tricks, IP address links, and internationalized or punycode hostnames.

Expected statuses:

- no URLs found: no URL-looking text was detected;
- no obvious local parsing risk found: the link still needs user judgment, but no local parsing rule flagged it;
- warning: the link needs review first;
- blocked: the link should not be opened.

## Open encrypted store

The Open encrypted store button calls the local API setup create endpoint.

The browser does not receive the vault passphrase. The local API uses the configured `LLH_VAULT_PASSPHRASE` and `LLH_APP_STORE` values.

Expected statuses:

- `created`: the encrypted store was created;
- `already_exists`: the encrypted store already exists;
- failure message: the local API could not create or open the configured store.

## Create test friend

The Create test friend button calls the local API test friend endpoint.

This creates a local two-sided test pair in the encrypted store so the playground can be tested without manual invite and response copy/paste.

This is for development and local interface testing only. A real friend still requires the Add friend invite flow and safety-number verification.

## Send test message

The Send test message button calls the local API test message endpoint.

It sends an encrypted local loopback message from the test friend to the generated peer contact, then records both the sent and received history entries in the encrypted local store.

This is for development and local interface testing only. It confirms the local store, session sealing, session opening, and UI refresh path without requiring manual relay steps.

## Prototype Add friend panel

The Add friend panel can call local API prototype actions through visible fields instead of browser prompt dialogs.

Fields:

- Friend name: the local name to save;
- Invite ID: filled after creating a friend invite;
- Friend invite JSON: paste a received friend invite here;
- Friend response JSON: paste a received friend response here.

Actions:

- Create test friend: creates a local verified test pair for development;
- Send test message: sends and receives a local encrypted loopback message for development;
- Create friend invite: creates a local invite and pending encrypted draft, fills the invite ID and invite JSON fields, and prints JSON for copy/paste testing;
- Accept friend invite: reads the friend name and invite JSON fields, saves a contact, fills the response JSON field, and prints response JSON;
- Finish adding friend: reads the invite ID, friend name, and response JSON fields, then saves the paired contact.

This is still a prototype flow. A future interface should replace JSON copy/paste with guided screens and file import/export for real friend setup.

## Setup states

The local setup panel may show:

- `ready`: encrypted store exists and at least one contact is available;
- `empty_store`: encrypted store exists but no contacts are available;
- `missing_store`: the local API is running but the configured store file is missing;
- demo mode: the local API is not connected.

## Important setup note

The local API can now create the configured encrypted app store. Contact setup can be exercised through Create test friend or prototype Add friend actions, but the UI still needs a guided, polished setup flow before non-developer friend testing.

## Friend testing readiness

Do not ask a non-developer friend to test the full workflow yet. The interface still needs:

- guided Add friend screens instead of JSON copy/paste;
- UI-based safety-number comparison;
- clearer setup guidance;
- packaged app startup;
- real attachment transfer through the UI.

For now, friend testing should wait until the setup is simpler and the interface can create or import the needed local state without manual JSON copy/paste.

## Security guidance

Use harmless test messages and sample files only. Do not use sensitive real-world messages while the project remains a prototype and review candidate.
