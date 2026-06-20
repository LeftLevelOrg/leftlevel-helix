# Metrics Retention Policy

This is a draft metrics retention policy for product planning and legal review.

## Product rule

Retain aggregate metrics only.

Do not retain raw event logs for product analytics.

Do not retain message content, contact names, URLs, filenames, safety numbers, fingerprints, precise location, or device identifiers in metrics systems.

## Retention categories

Draft retention limits:

- essential service aggregate metrics: up to 730 days;
- optional product aggregate metrics: up to 365 days;
- security and abuse aggregate metrics: up to 1095 days;
- local-only user-visible counters: kept locally only and not uploaded.

These periods are draft limits and require legal review before production.

## Raw event logs

Raw event logs should not be retained for product analytics.

If temporary diagnostic logging is ever needed, it must be separately designed, clearly limited, reviewed, and must not include forbidden private fields.

## Forbidden retained fields

Metrics retention systems must not retain:

- message content;
- message text;
- contact names;
- friend names;
- URLs;
- hostnames;
- IP addresses tied to users;
- device IDs;
- advertising IDs;
- install IDs;
- session IDs;
- filenames;
- attachment hashes;
- safety numbers;
- peer fingerprints;
- precise location.

## Local-only counters

Local-only counters may be stored in the user's encrypted local store for user-visible diagnostics and testing.

They should not be uploaded unless they pass the privacy metrics contract, meet aggregation requirements, and fall under either essential service metrics or optional opt-in telemetry.

## Deletion and aggregation

Draft direction:

- aggregate further when detailed aggregate slices are no longer needed;
- delete expired aggregate metrics on schedule;
- do not keep raw product analytics event logs;
- keep retention rules visible in release readiness review.

## Release boundary

Before production release:

- legal review must approve retention periods;
- privacy notice must disclose retention at an appropriate level;
- terms language must align with the privacy notice;
- app store disclosures must be accurate;
- tests must confirm no forbidden fields are retained;
- production metrics schemas must be reviewed against this policy.
