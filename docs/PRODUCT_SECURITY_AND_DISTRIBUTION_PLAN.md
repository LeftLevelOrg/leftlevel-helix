# Product, Security, and Distribution Plan

This document turns LeftLevel Helix from a protocol prototype into a usable, distributable product plan.

## Product promise

LeftLevel should be a private messaging system where users do not need phone numbers, email addresses, or central accounts to establish encrypted conversations.

The strongest product line is:

> Private by design. Server-blind by default. Built to stay online.

## What must feel easy

- Create an identity.
- Invite someone.
- Verify the contact.
- Send a message.
- Receive a message.
- Understand whether the contact is verified.
- Recover from reinstall or device change safely.
- Know what the app does and does not protect.

## Website sections to build

1. Hero: what LeftLevel is.
2. How it works: invite, verify, message.
3. Protection matrix: what it protects and what it does not.
4. Protocol page: technical overview for engineers.
5. Download page: desktop/mobile builds when ready.
6. Developers page: CLI, relay, integrations, API.
7. Security page: audits, threat model, responsible disclosure.
8. Integrations page: Discord, Slack, browser, mobile share sheet.
9. FAQ: plain-language answers.
10. Roadmap: transparent maturity status.

## Release channels

### Prototype

- GitHub source.
- CLI package.
- Demo relay.
- Explicit prototype warnings.

### Alpha

- Desktop app.
- Local encrypted store.
- Contact verification.
- Manual update flow.
- Test relay only.

### Beta

- Signed desktop builds.
- Mobile preview.
- Public relay beta.
- Basic integrations.
- Security review in progress.

### Production

- Independent audit.
- Signed releases.
- Reproducible builds.
- Mobile app store releases.
- Responsible disclosure program.
- Public security whitepaper.

## Security work before production

- Independent cryptography review.
- Formal protocol review.
- OWASP MASVS-aligned mobile review.
- Endpoint hardening.
- Key-change warnings.
- Secure local database.
- Device migration design.
- Fuzz testing.
- Static analysis.
- Supply-chain hardening.
- Reproducible builds.

## UX work before production

- Trust status badges.
- Safety-number comparison UI.
- QR verification.
- Plain-language warnings.
- No plaintext notifications by default.
- Invite flow that non-technical users can complete.
- Clear recovery flow.
- Accessible onboarding.

## Protocol work before production

- Header encryption so only mailbox ID is relay-visible.
- Periodic post-quantum rekey.
- Contact trust state.
- Encrypted message history.
- Multi-device model.
- Attachment encryption and chunking.
- Relay rotation.
- Small group protocol research.

## Integration work before production

- Deep links.
- Website invite links.
- Discord app for discovery and launch.
- Notification-only integrations.
- Minimal-scope OAuth policies.
- Integration privacy labels.

## Documentation standards

Every public claim should be labeled as one of:

- Implemented in prototype.
- Planned.
- Requires audit.
- Out of scope.

Avoid these claims until proven:

- Unhackable.
- Fully anonymous.
- Metadata-free.
- Secure against compromised devices.
- Production ready.

## Near-term build order

1. Contact trust store.
2. Automated verification request and confirmation messages.
3. Encrypted local message history.
4. Full live-relay CLI integration test.
5. Website security pages generated from these docs.
6. Desktop UI shell.
