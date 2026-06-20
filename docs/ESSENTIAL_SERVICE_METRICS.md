# Essential Service Metrics

LeftLevel needs a small set of mandatory operational metrics to run, support, secure, and scale the service.

These are different from optional product-improvement telemetry.

## Product rule

Essential service metrics may be mandatory when they are:

- necessary to operate the service;
- clearly disclosed in the privacy notice and terms;
- aggregate counters only;
- not used for advertising;
- not used for cross-app tracking;
- not sold or shared with data brokers;
- not used to infer private social graphs.

## Allowed essential service metrics

Allowed mandatory service counters include:

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

These counters help operate the service, estimate infrastructure needs, detect outages, support reliability, and detect abuse.

## Forbidden data

Essential service metrics must not include:

- message content;
- contact names;
- friend names;
- phone numbers;
- email addresses;
- URLs;
- hostnames;
- IP addresses tied to users;
- device IDs;
- advertising IDs;
- install IDs;
- session IDs;
- precise location;
- filenames;
- attachment hashes;
- safety numbers;
- peer fingerprints.

## Consent and notice

Essential service metrics do not need to be opt-in when they are truly necessary to operate the service and are properly disclosed.

They still require clear notice.

Optional product-improvement telemetry should remain opt-in.

## User-facing explanation

Recommended language:

> LeftLevel collects limited aggregate service metrics needed to operate, secure, and support the service, such as total message counts, delivery failures, abuse report counts, and blocked-link counts. These metrics do not include message content, contact names, links, files, device identifiers, precise location, safety numbers, or peer fingerprints.

## Boundary from optional telemetry

Essential service metrics:

- mandatory;
- disclosed in terms and privacy notice;
- aggregate only;
- needed to operate the service.

Optional telemetry:

- opt-in;
- used for product improvement;
- still aggregate only;
- never includes content or identifiers.

## Release boundary

Before enabling mandatory service metrics in production:

- privacy notice text must be complete;
- terms language must be complete;
- exported fields must be reviewed;
- no forbidden fields may appear in payloads;
- deletion/retention rules must be documented;
- security review must confirm metrics cannot reveal message content or social graphs.
