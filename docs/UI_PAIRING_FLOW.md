# UI Pairing Flow

This document describes the intended pairing flow for the future app interface.

## Current status

The current interface does not yet perform full pairing from the UI.

The local API now reports pairing readiness through setup status so the UI can show whether pairing is blocking interface testing.

## Pairing states

The setup status response includes a `pairing` object with:

- status format version;
- pairing state;
- user-facing label;
- next action;
- whether the state blocks friend testing.

Current states:

- `needs_pairing`: no paired contacts are available;
- `paired_contacts_available`: at least one paired contact is available.

## UI behavior

The interface should:

1. Show pairing state in the local setup panel.
2. Block friend-testing readiness when no paired contacts exist.
3. Guide the user to create or import a paired session.
4. Require safety-number comparison before sensitive use.
5. Keep pairing material in the local API or local app process, not in a public relay-visible field.

## Future pairing milestones

The future UI should support:

- create encrypted local store;
- generate invite file or invite text;
- import response file or response text;
- save paired contact into the encrypted local store;
- display safety number;
- mark contact verified only after user comparison;
- warn when safety number changes.

## Security boundary

The UI should not invent or alter protocol identity state. It should call Helix interfaces for invite creation, response processing, session storage, and safety-number generation.

Pairing UX must preserve the security-first rule: clear verification before trust.
