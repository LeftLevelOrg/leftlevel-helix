# Versioning Policy

LeftLevel Helix uses versioning to protect compatibility, reviewability, and user safety.

## Version categories

### Package version

The package version identifies a release of the reference implementation.

It should change when code, tests, documentation, or public APIs change in a way that should be tracked by release notes.

### Wire protocol name

The wire protocol name identifies the message and session protocol family.

Changing the wire protocol name should be rare. It should only happen when interoperability or security behavior changes in a way that older clients cannot safely process.

### Payload format versions

Payload format versions identify specific serialized structures, such as attachment references, transfer packages, integrity reports, and local data formats.

Payload format versions should change when a serialized structure changes in a way that affects parsing, verification, or compatibility.

## Compatibility rules

- Do not silently change serialized formats.
- Keep backward parsing only when it is safe and tested.
- Reject unsupported versions explicitly.
- Document migration behavior before changing storage formats.
- Keep protocol test vectors for reviewable compatibility checks.

## Pre-1.0 status

Before version 1.0, the project may still make breaking changes while the design is reviewed.

Even before 1.0, breaking changes should be documented clearly in the changelog and release notes.

## Production status

A version number alone does not indicate production readiness.

Production readiness requires completion of the release readiness gates and a signed-off release record.

## Release tag format

Recommended tag format:

```text
vMAJOR.MINOR.PATCH
```

Examples:

```text
v0.8.0
v0.8.1
v1.0.0
```

## Changelog rule

Every release candidate should update `CHANGELOG.md` with:

- summary;
- protocol changes;
- local API changes;
- storage changes;
- relay changes;
- user interface changes;
- known limitations;
- readiness status.
