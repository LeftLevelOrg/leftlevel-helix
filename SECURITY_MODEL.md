# Security Model

## Strong claims for v0.2 prototype

When implemented and run correctly:

- The relay cannot decrypt message contents.
- A stolen relay database does not contain plaintext messages.
- Tampering with ciphertext or authenticated headers is detected.
- Replay of an already-consumed envelope is rejected.
- Session establishment uses both classical X25519 and post-quantum ML-KEM-768 material.
- Message keys are single-use and deleted by ratcheting state forward.

## Threats addressed

| Threat | v0.2 posture |
|---|---|
| Passive network eavesdropping | Message contents encrypted. |
| Relay server compromise | Contents remain encrypted. |
| Relay database theft | Only encrypted envelopes and mailbox IDs. |
| Harvest-now-decrypt-later quantum risk | Hybrid X25519 + ML-KEM-768 mitigates this. |
| Message tampering | AEAD authentication rejects it. |
| Message replay | Consumed mailbox IDs reject replay. |
| No phone/email identity exposure | No phone/email required. |

## Threats not fully addressed yet

| Threat | Current status |
|---|---|
| Compromised phone/laptop | Not solved by protocol. Requires endpoint hardening. |
| Malicious keyboard/screen reader/overlay | Future secure-compose work. |
| Screenshots or camera pointed at screen | Cannot be cryptographically prevented. |
| Global traffic analysis | Needs mix routing, cover traffic, or onion routing. |
| Large group compromise recovery | Future group protocol needed. |
| Out-of-order message delivery | Future skipped-key cache needed. |
| Metadata-free relay operation | v0.2 minimizes metadata but does not eliminate timing/IP metadata. |

## No-logs relay posture

A production relay should:

- Avoid request body logging.
- Avoid IP logging where legally and operationally possible.
- Store short-lived encrypted envelopes only.
- Use strict TTLs.
- Use blind rate-limits or anonymous tokens instead of user accounts.
- Support multiple independent relays.

## Endpoint hardening roadmap

Future app builds should add:

- encrypted local message store
- app lock
- hidden notification previews
- screenshot/screen-recording blocking where supported
- secure compose fields
- clipboard clearing
- accessibility-overlay warnings
- optional disappearing messages
- optional local-only mode
