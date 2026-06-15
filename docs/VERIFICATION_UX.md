# Verification UX Plan

LeftLevel should make verification feel simple while still being honest about trust.

## Core principle

Verification can be assisted and made seamless, but first-contact trust cannot be fully automated unless there is already another trusted identity channel.

The app should automate everything except the final trust decision.

## Verification levels

| Level | User-facing label | Meaning |
|---|---|---|
| Unverified | New contact | A session exists, but the user has not confirmed the other person. |
| Assisted verification pending | Waiting for confirmation | The app has sent a verification request to the other party. |
| Verified | Verified contact | Both sides confirmed the same safety number or QR verification. |
| Changed | Safety number changed | The contact's safety number changed. The app must warn before sending sensitive content. |

## Seamless verification flow

1. Alice creates an invite.
2. Bob accepts it.
3. Both apps compute the same safety number from the signed handshake transcript.
4. Alice sees a button: **Verify Bob**.
5. Alice taps it.
6. Bob receives: **Alice wants to verify this session**.
7. Both apps display the same short code and QR option.
8. Bob taps **Matches** only if the code matches Alice's screen or voice call.
9. Both apps mark the contact as verified.

## Button-based verification request

A verification request can be sent through the encrypted session after the first handshake:

```json
{
  "type": "verification_request",
  "conversation_id": "...",
  "safety_fingerprint": "...",
  "requested_at": "..."
}
```

The response should also be encrypted:

```json
{
  "type": "verification_ack",
  "conversation_id": "...",
  "safety_fingerprint": "...",
  "result": "matches"
}
```

This confirms both apps see the same safety fingerprint, but it does not prove the real-world identity unless the users trust the comparison path. The UI must explain that clearly.

## Best UX options

### QR scan

Best for in-person verification. One device displays a QR code containing the safety fingerprint. The other scans it.

### Voice call phrase

Best for remote verification. The app shows a short phrase or grouped numeric code. Users compare it over a voice/video call.

### Button confirmation

Good for low-friction confirmation after a trusted side channel has already been used. The button should never silently mark a contact verified without a user action.

### Contact change warnings

If a contact's safety number changes, the app should show a clear warning:

> This contact's safety number changed. This can happen after reinstalling or adding a new device, but it can also mean someone is trying to intercept the conversation. Verify before sending sensitive messages.

## What not to do

- Do not silently auto-verify first contact.
- Do not hide changed safety numbers.
- Do not claim that a button alone proves identity.
- Do not rely on Discord, email, SMS, or a relay as the sole proof of identity.
- Do not train users to ignore safety warnings.

## Recommended v0.5 implementation

- Store contact trust state locally.
- Add `verified`, `unverified`, and `changed` states.
- Add CLI command: `leftlevel-verify request`.
- Add CLI command: `leftlevel-verify confirm`.
- Add QR payload format.
- Add tests proving safety-number changes trigger `changed` state.
