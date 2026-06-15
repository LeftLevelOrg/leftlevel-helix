# Repository Strategy

LeftLevel should keep security-critical protocol work easy to review while still allowing the user interface and public website to evolve quickly.

## Recommended repository boundaries

### `leftlevel-helix`

Purpose: protocol core, security model, reference implementation, test vectors, local API contracts, and reference relay behavior.

This repository should contain:

- cryptographic/session code;
- protocol documents;
- security model documents;
- test vectors and fixtures;
- local API contract definitions;
- reference relay behavior;
- desktop playground prototypes while API boundaries are still changing.

It should remain security-first and review-focused.

### `leftlevel-app`

Purpose: the real user-facing desktop and mobile app experience.

This repository should contain:

- production UI code;
- onboarding and pairing screens;
- contact management screens;
- safety-number comparison screens;
- send and receive flows;
- attachment integrity UI;
- packaged desktop/mobile builds;
- app-specific tests and release workflows.

Create this repository when the local API and pairing flow are stable enough that the interface can evolve without changing core protocol internals on every step.

### `leftlevel-website`

Purpose: public website, landing pages, project messaging, downloads, and roadmap.

This repository should contain:

- homepage and marketing pages;
- public documentation landing pages;
- download and setup pages;
- public roadmap and status pages;
- website-specific design assets.

The website should follow `docs/WEBSITE_MESSAGING_BRIEF.md` and avoid overstated security claims.

### `leftlevel-relay`

Purpose: production relay service and deployment hardening, if relay operations become a separate product concern.

This repository may later contain:

- production relay service code;
- deployment manifests;
- monitoring guidance;
- abuse-prevention controls;
- operational hardening docs.

Until then, the reference relay can remain in `leftlevel-helix`.

## Split timing

### Keep the playground in this repository for now

The playground should remain in `apps/desktop-playground` while the protocol, local API, attachment model, and UI expectations are still changing together.

This keeps early iteration fast and prevents premature duplication between repositories.

### Create `leftlevel-app` when the interface can run a real local test flow

The app repository should be created when the interface can support:

- opening or creating an encrypted local store;
- pairing or importing a paired session;
- displaying and comparing safety numbers;
- sending and receiving non-sensitive test messages;
- showing message status and failure states;
- showing attachment verification states from real local data.

### Keep the protocol boundary stable before app split

Before moving the UI into `leftlevel-app`, Helix should provide stable integration points such as:

- local API endpoints;
- protocol test vectors;
- documented message and attachment payload contracts;
- documented trust and integrity status values;
- a clear versioning policy.

## Security-first rule

Protocol code, security claims, and integrity behavior should remain in the core repository until reviewed and well documented.

The app repository should consume those behaviors rather than reimplementing them independently.

## Documentation rule

When the app repository is created, keep `leftlevel-helix` as the source of truth for security model, protocol behavior, and public claim boundaries.

Website and app documentation should link back to the protocol/security docs rather than inventing separate claims.
