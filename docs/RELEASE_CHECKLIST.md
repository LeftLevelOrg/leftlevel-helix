# Release Checklist

Use this checklist for release candidates. Completing this checklist does not by itself approve production use; it creates the evidence package for review.

## Prepare release candidate

- Confirm version label.
- Update `CHANGELOG.md`.
- Confirm `docs/VERSIONING_POLICY.md` still matches the release behavior.
- Confirm known limitations are documented.

## Run validation

- Run portable tests.
- Run release readiness document validation.
- Run any environment-specific tests that are available.
- Save test summary evidence.

## Build artifacts

- Build source archive.
- Build Python package artifact.
- Generate artifact manifest with checksums.
- Store artifact names and hashes in release notes.

Example manifest command:

```bash
python scripts/generate_artifact_manifest.py dist/* --version v0.8.0-rc1 --out artifact-manifest.json
```

## Review evidence

- Protocol evidence linked.
- Implementation evidence linked.
- Storage evidence linked.
- Relay evidence linked.
- User interface evidence linked.
- Release evidence linked.
- Documentation evidence linked.

## Sign-off

- Complete `docs/SIGNOFF_RECORD_TEMPLATE.md`.
- Record decision as approved, rejected, or deferred.
- Do not mark production-ready unless every readiness gate is complete.

## Publish

- Publish artifacts only after approval.
- Publish checksums and verification instructions.
- Publish changelog and known limitations.
- Keep public website status aligned with repository status.
