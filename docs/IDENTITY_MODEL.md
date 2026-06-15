# Identity Model

LeftLevel does not require global public user IDs such as phone numbers, email addresses, or usernames.

It still has identifiers, but they are local, pseudonymous, and pairwise.

## Why no global ID?

Global IDs make products convenient, but they also create a directory of people. If every message, device, or relay request points back to the same global account, the system becomes easier to track.

LeftLevel's design goal is different: let two people establish a private relationship without forcing them into a central account directory.

## The identifiers LeftLevel does use

| Identifier | Where it lives | Who sees it | Purpose |
|---|---|---|---|
| Local contact name | User's encrypted app store | Local user only | Human label such as `bob` or `alice` |
| Identity signing key | User device and invite/response | The paired contact | Pseudonymous contact identity |
| Safety number | User devices | Both paired users | Verification against impersonation |
| Conversation/session state | Encrypted app store | Local user only | Ratchet keys and counters |
| Mailbox ID | Relay | Relay and recipient | One-time delivery lookup |

## Example

Alice adds Bob as a contact.

On Alice's device:

```text
contact name: bob
trust state: OK
safety number: 123-456-789-012
session state: encrypted locally
```

On the relay:

```text
mailbox_id: BQ4sN...random-looking...
ciphertext: encrypted envelope
```

The relay does not need to know Alice, Bob, a phone number, an email, or a permanent username.

## Renaming contacts

A contact name is only a local label. If Alice renames `bob` to `robert`, the connection does not change.

The app preserves:

- session state;
- ratchet counters;
- trust state;
- safety number;
- peer identity fingerprint;
- sent and received message history.

Only the local display name changes.

The CLI command is:

```bash
leftlevel-app rename-contact bob robert
```

This does not notify the other person because it is not a protocol identity change. It is the same as changing a nickname in an address book.

## How two people find each other

LeftLevel uses an invite flow:

1. Alice creates an invite.
2. Alice gives Bob the invite through some channel.
3. Bob accepts the invite and creates a response.
4. Alice finalizes the session.
5. Both compare the safety number before trusting the contact.

The invite/response exchange creates a pairwise secure relationship. It is not a public account registration.

## What happens if someone reinstalls?

A reinstall may create a new identity key and a new safety number. The app should show this as `CHANGED`, not silently trust it.

Users should re-verify the contact before sending sensitive messages.

## Future options

Later, LeftLevel can add optional discovery helpers such as:

- invite links;
- QR codes;
- contact cards;
- device pairing;
- trusted directory services;
- organization-managed directories.

Those should remain optional so the core privacy model does not depend on global identifiers.
