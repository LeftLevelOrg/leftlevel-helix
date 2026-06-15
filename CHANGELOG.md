# Changelog

All notable changes to LeftLevel Helix should be documented here.

## Unreleased

### Status

- Current status: prototype and review candidate.
- Not approved for production use.
- Not independently audited.

### Added

- Security-first project values.
- Website messaging brief for future public site updates.
- Repository strategy for protocol, app, website, and relay separation.
- UI extraction plan for the future `leftlevel-app` repository.
- UI pairing flow documentation.
- Release readiness gates and sign-off template.
- Local interface testing guide.
- Local API setup status endpoint.
- Local API pairing actions for invite, accept, and finalize.
- Pairing status contract for setup readiness.
- App-store pairing draft storage.
- Desktop playground local setup status panel.
- Desktop playground pairing guidance in setup panel.
- Desktop playground prototype pairing action panel.
- Desktop playground attachment integrity panel.
- Local API send and receive endpoints.
- Playground send and receive button wiring.
- Encrypted attachment store.
- Opaque attachment transfer packages.
- Attachment integrity reports.

### Changed

- Desktop playground now displays trust states, setup readiness, pairing guidance, attachment states, and local API send and receive status messages.
- Documentation now emphasizes security first, then fast and usable messaging.

### Known limitations

- The interface is still a playground, not a packaged app.
- Pairing uses prototype prompt dialogs and JSON copy/paste, not polished guided screens.
- Safety-number comparison is not yet fully UI-driven.
- Attachment transfer is not yet fully wired through relay-backed UI flows.
- Release artifacts are not yet signed.
- Production readiness gates are incomplete.

## v0.6.0

### Added

- Sealed message metadata.
- Encrypted local app store.
- Contact trust labels.
- Local contact rename support.
- HTTP relay client and CLI workflows.
- Safety-number verification helpers.
- Protocol and security documentation.

### Status

- Prototype release.
- Not production-ready.
