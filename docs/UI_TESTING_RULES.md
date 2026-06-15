# UI Testing Rules

The desktop playground has smoke tests that protect user-facing wording and visible safety states.

## Wording changes

When visible UI wording changes, update the matching tests in the same change.

Examples:

- changing `Pairing` to `Add friend` requires updating the playground static tests;
- changing a button label requires updating button-label assertions;
- changing status text requires updating status-text assertions.

## Color and text indicators

The UI should not rely on color alone. Tests should check both the visible text and the CSS class used to style it.

The current user-facing meanings are:

- green means verified;
- yellow means review first;
- red means stop and check.

## Expected failures during iteration

A UI smoke test failure after an intentional wording change usually means the test is doing its job.

The fix is to confirm the new wording is intentional, then update the test expectation in the same commit.

## Friend-facing language

Prefer user-friendly words in the app:

- Add friend;
- friend invite;
- finish adding friend;
- verified;
- review first;
- stop and check.

Technical terms can remain in protocol and developer documentation where precision is needed.
