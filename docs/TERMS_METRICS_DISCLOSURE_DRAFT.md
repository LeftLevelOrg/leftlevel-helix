# Terms Metrics Disclosure Draft

This is draft terms language for product planning and legal review. It is not final production terms.

## Service operations metrics

To provide, secure, support, and improve service reliability, LeftLevel may collect and process limited aggregate service operations metrics.

These metrics may include aggregate counts such as:

- registered users total;
- active users estimate;
- messages sent total;
- messages received total;
- relay envelopes stored;
- relay envelopes fetched;
- delivery failures total;
- aggregate errors total;
- abuse reports total;
- links blocked total;
- attachments blocked total.

These metrics are mandatory because they are needed to operate, secure, support, and scale the service.

## Limits on service metrics

Service operations metrics must not include:

- message content;
- contact names;
- friend names;
- URLs from messages;
- hostnames from messages;
- filenames;
- attachment hashes;
- safety numbers;
- peer fingerprints;
- precise location;
- advertising identifiers;
- device identifiers used for cross-app tracking.

## Optional product telemetry

LeftLevel may offer optional product-improvement telemetry.

Optional telemetry is separate from mandatory service operations metrics and should require the user's choice before remote export.

Optional telemetry must remain aggregate-only and must not include message content, contact identifiers, links, files, safety numbers, fingerprints, device IDs, advertising IDs, or precise location.

## No advertising or data broker use

LeftLevel service metrics and optional telemetry must not be sold to data brokers or used for advertising, cross-app tracking, or inferring private social graphs.

## Security and abuse prevention

LeftLevel may use aggregate safety counters, such as blocked-link counts, attachment-block counts, delivery-failure counts, and abuse-report counts, to protect the service and its users.

These counters must not include message content, link destinations, file contents, or contact identities.

## Legal review required

Before production release, this language must be reviewed by qualified counsel and aligned with the final privacy notice, app store disclosures, retention rules, and regional privacy requirements.
