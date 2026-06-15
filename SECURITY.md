# Security Policy

LeftLevel Helix is security-sensitive software. Please report suspected vulnerabilities privately.

## Supported versions

| Version | Status |
|---|---|
| v0.x | Research prototype; not production-ready |

No version is currently approved for sensitive real-world use.

## Reporting a vulnerability

Please do not open a public GitHub issue for a suspected vulnerability.

For now, report privately to the project owner/maintainers through the safest available contact channel listed on the LeftLevel project or GitHub organization profile.

A future version should add a dedicated security email address and publish a signed `security.txt` file.

## What to include

Please include:

- affected version or commit;
- clear reproduction steps;
- expected behavior;
- observed behavior;
- impact assessment;
- proof-of-concept details, if safe to share;
- whether the issue affects cryptography, relay privacy, local storage, identity verification, or endpoint behavior.

## Handling process

1. A maintainer acknowledges the report.
2. The issue is triaged for severity and scope.
3. A private fix branch is prepared if needed.
4. Tests and documentation are updated.
5. A release note or advisory is published when appropriate.

## Security boundaries

Please remember that the current prototype does not claim to protect against:

- compromised devices;
- malicious keyboards or screen readers;
- screenshots or cameras pointed at the screen;
- unverified first-contact impersonation;
- global traffic analysis;
- production-grade relay abuse.

See `docs/PROTECTION_MATRIX.md` for the current protection model.
