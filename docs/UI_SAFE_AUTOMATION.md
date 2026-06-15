# UI Safe Automation

The interface should automate safe decisions where possible and ask the user only when trust needs review.

## Send behavior

The current send rule is:

- green friend: send normally;
- yellow friend: ask before sending;
- red or changed friend: stop sending until the friend is checked again.

This gives the app a simple default path while still protecting users when the friend state is uncertain or changed.

## Verify behavior

The Verify action asks the user to confirm they compared the safety number before the friend becomes green.

The app should not silently mark a friend verified.

## User guidance

Every automated stop or warning should tell the user what happened and what to do next.

Examples:

- `green means verified`;
- `yellow means review first`;
- `red means stop and check`;
- `compare safety numbers first`.

## Rule

Automate routine safe paths. Require confirmation for trust changes. Stop when the app cannot verify enough to continue safely.
