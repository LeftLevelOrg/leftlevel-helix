# Release Artifact Policy

This policy describes the expected release artifact process for LeftLevel Helix once the project begins producing release candidates.

## Current status

Current status: prototype and review candidate.

Release artifacts are not yet production artifacts.

## Required artifacts for a release candidate

A release candidate should include:

- source archive;
- Python package artifact;
- test report summary;
- changelog entry;
- dependency inventory reference;
- release readiness gate record;
- sign-off record;
- checksums for released files.

## Signing policy

Before production approval, release artifacts should be signed by an approved maintainer key.

The release notes should identify:

- signing key identity;
- artifact names;
- artifact checksums;
- verification instructions.

## Reproducible build plan

Before production approval, the project should document how to reproduce release artifacts from a clean checkout.

The plan should include:

- supported build environment;
- Python version;
- dependency lock or pin file;
- build command;
- expected artifact names;
- checksum verification process.

## SBOM plan

Before production approval, release candidates should include or link to a software bill of materials.

The SBOM should cover:

- direct dependencies;
- transitive dependencies where available;
- package versions;
- licenses;
- build tooling.

## Rollback policy

Each release candidate should document rollback guidance.

Rollback notes should include:

- prior recommended version;
- storage compatibility notes;
- protocol compatibility notes;
- relay compatibility notes;
- known migration risks.

## Publication rule

Do not publish artifacts as production-ready unless the release readiness gates are complete and a sign-off record is approved.
