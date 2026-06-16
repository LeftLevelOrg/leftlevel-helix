# Link and Sandbox Policy

LeftLevel should assume that links and files from other people can be hostile.

This document defines the product safety direction for malicious URL handling, attachment handling, and operating-system isolation.

## Threat model

A hostile message may contain:

- a URL that attempts browser, WebView, or operating-system exploitation;
- a phishing link that tricks the user into giving away credentials;
- a file that exploits a parser, previewer, image library, PDF reader, archive tool, or media stack;
- social engineering text that pressures the user to open something quickly.

No messenger can guarantee that a compromised operating system remains safe. LeftLevel can still reduce the chance of exploitation and limit the blast radius when something goes wrong.

## Link safety rules

Default behavior:

- do not auto-link URLs in messages;
- render message bodies as plain text, not HTML;
- never use message text as `innerHTML`;
- never open a URL automatically;
- require an explicit user action before a URL leaves the app;
- show the full destination before opening;
- prefer a warning screen before opening an external browser;
- allow users to copy link text without making it clickable.

Current playground behavior:

- message bodies are rendered with `textContent`;
- links are shown as plain text;
- links are not made clickable automatically;
- local link inspection can flag obvious parsing risks without opening the URL.

## Local link inspection

Local inspection should never fetch the website.

It may inspect:

- URL scheme;
- normalized host;
- localhost or private-network targets;
- plain HTTP;
- username/password text before the host;
- IP address links;
- internationalized or punycode hostnames.

Local inspection can block obvious risky links, but it cannot prove a URL is safe.

## Isolated URL validation

Remote or active validation should run only in a disposable isolated worker, not in the main app.

An isolated URL validation worker should have:

- no vault access;
- no contacts access;
- no message history access;
- no user cookies;
- no user browser profile;
- no local-network access;
- no host filesystem write access except a temporary scratch directory;
- no access to platform secrets;
- a short timeout;
- a fresh identity for each scan;
- outbound network limited to the target and approved reputation services.

The worker may collect:

- redirect chain;
- final host;
- TLS certificate summary;
- MIME type;
- response size limits;
- known-malware or known-phishing reputation results;
- whether the page tries to trigger downloads;
- whether the page tries to navigate to disallowed schemes.

The worker must return a label such as `blocked`, `warning`, or `no obvious risk found`. It must not return `safe`, because scanners can miss zero-days and social engineering.

## Attachment safety rules

Default behavior:

- do not preview unsafe or unverifiable files automatically;
- verify attachment integrity before opening;
- block known-bad or unverifiable attachments;
- open files outside the message renderer when possible;
- prefer download/quarantine style handling over inline rendering;
- avoid parsing complex formats inside the main UI process.

## Isolation direction

The production architecture should separate privileges:

- message renderer: no direct vault access and no direct filesystem access;
- local API or core service: owns vault access and crypto operations;
- attachment processor: separate sandboxed process with minimal permissions;
- link opener: explicit user-confirmed external handoff;
- relay: sees encrypted envelopes only.

## Desktop sandbox direction

A packaged desktop app should aim for:

- renderer sandboxing enabled;
- context isolation enabled;
- no Node integration in the renderer;
- strict Content Security Policy;
- no remote code loading;
- no automatic URL opening;
- restricted filesystem permissions;
- separate process for risky attachment handling.

## Mobile sandbox direction

A mobile app should aim for:

- use the native OS app sandbox;
- do not use broad storage permissions;
- do not auto-open links;
- do not render message HTML in a WebView;
- use platform safe browsing APIs where available;
- keep secrets in platform-backed secure storage;
- isolate attachment previewing from the core message store.

## Container limits

Containers and app sandboxes can reduce damage, but they are not a guarantee against a full device compromise.

If the operating system kernel, browser engine, WebView, or privileged service is compromised, the attacker may escape the app boundary. LeftLevel should still design for least privilege so a single message renderer failure does not automatically expose the vault, keys, contacts, or attachments.

## Product rule

Do not make hostile content convenient to execute.

Show messages safely as text, make risky actions deliberate, and isolate the parts of the app that must handle untrusted content.
