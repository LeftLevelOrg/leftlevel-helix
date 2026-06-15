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
- UI security-language guide for simple user wording and green/yellow/red indicators.
- UI safe-automation guide for green/yellow/red send behavior.
- Release readiness gates and sign-off template.
- Local interface testing guide.
- Local API setup status endpoint.
- Local API encrypted store create endpoint.
- Local API pairing actions for invite, accept, and finalize.
- Pairing status contract for setup readiness.
- App-store pairing draft storage.
- Desktop playground local setup status panel.
- Desktop playground Open encrypted store automation.
- Desktop playground pairing guidance in setup panel.
- Desktop playground guided Add friend fields.
- Desktop playground prototype Add friend action panel.
- Desktop playground security indicator legend.
- Desktop playground send safety guard.
- Desktop playground attachment integrity panel.
- Local API send and receive endpoints.
- Playground send and receive button wiring.
- Encrypted attachment store.
- Opaque attachment transfer packages.
- Attachment integrity reports.

### Changed

- Desktop playground now uses user-facing Add friend language instead of protocol pairing language.
- Desktop playground now uses visible Add friend fields instead of prompt dialogs for invite and response JSON.
- Desktop playground now displays trust states, setup readiness, pairing guidance, attachment states, and local API send and receive status messages.
- Documentation now emphasizes security first, then fast and usable messaging.

### Known limitations

- The interface is still a playground, not a packaged app.
- Add friend still uses JSON copy/paste, not polished guided screens or file import/export.
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
