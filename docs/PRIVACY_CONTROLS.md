# Privacy Controls

This document defines the user-facing privacy controls for metrics and telemetry.

## Product rule

Essential service metrics are mandatory disclosed operations metrics.

Optional product-improvement telemetry is off by default and user-controllable.

Local diagnostics are local-only and user-visible.

## Essential service metrics

Essential service metrics are required to operate, secure, support, and scale the service.

They cannot be disabled in the app because they are necessary service operations metrics.

They still require clear notice in the privacy notice and terms.

Essential service metrics must remain aggregate-only and must not contain message content, contact names, links, files, device identifiers, safety numbers, peer fingerprints, or precise location.

## Optional product telemetry

Optional product telemetry helps improve the app experience.

It should default off.

The user must be able to turn it on or off.

Remote optional telemetry export must not run unless the setting is enabled and the export payload passes the privacy telemetry export contract.

## Local diagnostics

Local diagnostics may show aggregate counts to the user on their own device.

Local diagnostics should not upload anything by default.

Examples:

- local friend counts;
- local sent and received message counts;
- local blocked-link counts;
- local blocked-attachment counts.

## Settings copy

Recommended settings language:

### Essential service metrics

> Required: limited aggregate service metrics used to operate, secure, support, and scale LeftLevel. These do not include message content, contact names, links, files, device identifiers, precise location, safety numbers, or peer fingerprints.

### Optional product telemetry

> Optional: share aggregate product-health counts to help improve LeftLevel. This is off by default and can be turned off at any time. It never includes message content, contact names, links, files, device identifiers, precise location, safety numbers, or peer fingerprints.

### Local diagnostics

> Local only: show aggregate counts from this device for troubleshooting. These counts are not uploaded.

## Release boundary

Before production release:

- privacy notice text must describe required service metrics;
- terms language must describe required service metrics;
- optional telemetry settings UI must exist before optional export is enabled;
- local diagnostics must clearly say when data is local-only;
- tests must confirm optional telemetry defaults off;
- tests must confirm essential service metrics cannot include forbidden fields.
