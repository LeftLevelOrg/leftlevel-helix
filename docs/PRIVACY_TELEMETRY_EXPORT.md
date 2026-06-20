# Privacy Telemetry Export

LeftLevel may eventually export product-health metrics, but export must be opt-in, aggregate-only, and privacy-contract enforced.

This document defines the export boundary.

## Current status

Current implementation:

- privacy metrics contract exists;
- local-only metrics endpoint exists;
- telemetry export preparation stub exists;
- telemetry network upload is not implemented.

## Product rule

The app may count whether the product works.

The app must not export who someone is, who they talk to, what they say, what links they receive, what files they receive, where they are, or which exact device they use.

## Export requirements

Telemetry export must require:

- explicit user consent;
- an opt-in metrics batch;
- privacy metrics contract validation;
- minimum aggregation group size of at least 100;
- destination represented as a product label, not a URL or device/user identifier;
- no message content;
- no contact names;
- no URLs, hosts, or IP addresses;
- no device IDs, install IDs, advertising IDs, or session IDs;
- no filenames, attachment hashes, safety numbers, or peer fingerprints.

## Export stub behavior

The export stub prepares an envelope only after all checks pass.

The stub performs no network I/O.

A future uploader must call the export stub first and must upload only the returned envelope.

## Forbidden behavior

The product must not:

- upload raw event logs;
- upload per-user timelines;
- upload stable cross-context identifiers;
- silently enable telemetry;
- hide telemetry settings from the user;
- use telemetry to infer social graphs;
- include message text, contact identifiers, link destinations, or file metadata.

## User-facing language

Recommended settings copy:

> Help improve LeftLevel by sharing aggregate product-health counts. This never includes message content, contact names, links, files, device IDs, or precise location. You can turn this off at any time.

## Release boundary

Remote telemetry upload must not be enabled until:

- opt-in UI exists;
- export payload review exists;
- privacy policy text exists;
- aggregation threshold enforcement is tested;
- deletion/disable behavior is tested;
- release sign-off confirms no forbidden fields are exported.
