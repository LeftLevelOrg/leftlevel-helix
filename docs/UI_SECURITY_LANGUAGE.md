# UI Security Language

The user interface should make security understandable without requiring protocol knowledge.

## User-facing names

Use simple product words in the app:

- use `Add friend` or `Add contact` instead of `pairing`;
- use `friend invite` instead of `pairing invite`;
- use `finish adding friend` instead of `finalize response`;
- use `verified`, `review first`, and `stop and check` instead of internal verification codes.

Technical terms may remain in protocol, API, and implementation documentation where precision matters.

## Color indicators

The app should use consistent color meaning:

- green: verified or safe to continue;
- yellow: review before continuing;
- red: stop, blocked, changed, or cannot be verified.

Color should not be the only signal. Each color should also include text.

## Secure-by-default behavior

The UI should automate safe choices where possible.

When something cannot be verified, the UI should say so clearly and provide safe next steps.

Examples:

- block opening an attachment that fails integrity checks;
- ask the user to compare safety numbers before marking a friend verified;
- show a changed-state warning when identity safety changes;
- request a resend when a message or attachment cannot be verified.

## Learning behavior

The interface should teach as the user works. Short explanations are preferred over technical warnings.

Examples:

- `Green means verified.`
- `Yellow means review first.`
- `Red means stop and check.`
- `This friend is not verified yet. Compare safety numbers before sensitive messages.`
- `This attachment cannot be verified. Opening is blocked.`

## Security boundary

Simple UI language must not weaken the model. The app should still call Helix protocol and local API functions for identity, verification, storage, and attachment integrity behavior.
