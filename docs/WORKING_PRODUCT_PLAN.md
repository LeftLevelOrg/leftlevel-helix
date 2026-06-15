# Working Product Plan

This is the near-term plan for turning LeftLevel Helix into a usable product without overcomplicating the scope.

## Product focus

Build one simple thing well first:

1. Pair two people.
2. Verify the contact.
3. Send encrypted messages through a blind relay.
4. Receive encrypted messages.
5. Keep encrypted local contact and message history.
6. Make the protection status clear.

Integrations with Discord, Slack, browsers, and other tools should stay on the future roadmap until the core app is stable.

## What v0.5 adds

v0.5 adds a minimal encrypted local app store. The app store contains:

- contacts;
- serialized session state;
- trust status;
- safety-number metadata;
- local sent/received message history.

This is not a final production database, but it gives the prototype a product-shaped workflow.

## Minimal product commands

```bash
leftlevel-app init
leftlevel-app add-contact bob --session alice-session.llh.vault
leftlevel-app contacts
leftlevel-app verify-contact bob
leftlevel-app send bob "hello" --relay-url http://127.0.0.1:8787
leftlevel-app receive bob --relay-url http://127.0.0.1:8787
leftlevel-app history bob
```

## User-facing status labels

The first UI should only need three trust states:

| State | Meaning |
|---|---|
| NEW | Contact exists, but the safety number has not been verified. |
| OK | User marked the contact verified. |
| CHANGED | The saved safety fingerprint changed and the user should re-verify. |

## What stays later

- Discord integration.
- Slack integration.
- Browser extension.
- Mobile share sheet.
- Multi-relay routing.
- Groups.
- Large attachments.
- Complex account/device recovery.

## Next milestone

The next milestone should be a small desktop UI shell that uses the same app store and shows:

- contacts;
- trust badge;
- message history;
- compose box;
- send/receive buttons;
- verify contact button.
