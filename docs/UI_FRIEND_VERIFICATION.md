# Friend Verification UI

This document describes the user-facing friend verification behavior.

## User-facing goal

The app should make verification easy to understand:

- green means verified;
- yellow means review first;
- red means stop and check.

## Verify action

The playground now wires the `Verify` button to the local API when the local API is connected.

Expected behavior:

- the user selects a friend;
- the user chooses `Verify` after comparing the safety number;
- the local API marks the friend as verified;
- the contact list refreshes;
- the friend becomes green/verified.

In demo mode, the button only updates the preview state and clearly says it is demo behavior.

## Safety boundary

The app should not automatically mark a friend verified merely because the contact exists.

Verification should represent a user decision after checking the safety number.

## Future improvements

Future guided screens should:

- show both safety numbers side by side;
- explain how to compare them;
- only enable final verification after the user confirms they match;
- show a red warning if the safety state changes later.
