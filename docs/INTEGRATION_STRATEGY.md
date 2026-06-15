# Integration Strategy

LeftLevel should integrate with existing platforms without giving those platforms plaintext access to protected messages.

## Integration principle

Existing apps should be used for discovery, notifications, and launch points. Sensitive message content should stay inside LeftLevel sessions and relays.

## Discord integration model

Discord is a good first integration target because Discord supports apps, slash commands, message components, OAuth2, and webhooks. LeftLevel should not send plaintext sensitive messages into Discord.

### Safe Discord use cases

| Use case | Safe approach |
|---|---|
| Invite discovery | A Discord command can create or deliver an opaque LeftLevel invite link. |
| Verification prompt | A Discord app can send a button that says **Open LeftLevel to verify**. |
| Message notification | A Discord app can say **New LeftLevel message available** without including plaintext. |
| Server onboarding | A Discord bot can help a community install LeftLevel and explain privacy status. |
| Support workflow | Discord can provide support, docs links, and status updates. |

### Unsafe Discord use cases

| Use case | Why to avoid it |
|---|---|
| Sending plaintext secure messages through a bot | The bot and platform can access message content. |
| Treating Discord identity as proof of real-world identity | Accounts can be compromised or impersonated. |
| Posting safety numbers publicly | Public channels can be watched and manipulated. |
| Relying on Discord as the relay for sensitive content | Discord will still see platform metadata and bot interaction context. |

## Integration architecture

```text
Discord / Slack / website / app store
        |
        | discovery, launch, notification, opaque links
        v
LeftLevel app
        |
        | encrypted envelopes only
        v
LeftLevel relay network
```

## Recommended Discord v1 commands

```text
/leftlevel start
/leftlevel invite @user
/leftlevel verify @user
/leftlevel help
```

The bot should respond with buttons such as:

- **Open LeftLevel**
- **Copy Invite**
- **Verify in LeftLevel**
- **Learn What Is Protected**

## OAuth and permissions posture

Request the minimum Discord permissions needed. Avoid message-reading scopes unless there is a clear user-facing reason and approval path. The safest early version should use slash commands, buttons, and opaque links rather than reading users' messages.

## Other platform integrations

### Slack

Use as a launch and notification surface. Do not route plaintext secure messages through Slack.

### Matrix

Potentially useful for federation research, but LeftLevel should not assume Matrix rooms provide the same metadata model as LeftLevel.

### Email

Useful for account recovery or invite delivery only if users understand email is not private. Avoid sending plaintext secret content.

### Browser extension

Potentially useful for quick share and link handling. Needs careful review because browser extensions can become powerful endpoint-risk surfaces.

### Mobile share sheet

High-value usability feature. Lets users share text/files into LeftLevel without using copy/paste.

## Product recommendation

Build integrations in this order:

1. Website deep links.
2. Desktop/mobile app link handler.
3. Discord slash-command app for invite discovery and education.
4. Discord notification-only bot.
5. Slack notification-only app.
6. Browser extension only after endpoint hardening.

## Rules for every integration

- Never send plaintext secure messages to third-party platforms.
- Never treat third-party account identity as complete proof of trust.
- Use minimal OAuth scopes.
- Keep integration tokens out of message cryptography.
- Make privacy status visible in the UI.
- Log as little as possible.
- Make unlinking and token revocation easy.
