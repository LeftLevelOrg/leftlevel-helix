# Privacy Notice Draft

This is a draft for product planning and legal review. It is not a final production privacy notice.

## Plain-language summary

LeftLevel is designed to protect private messages.

We do not collect message content, contact names, friend names, links you receive, files you receive, safety numbers, peer fingerprints, precise location, advertising IDs, or device identifiers for analytics.

We collect limited aggregate service metrics needed to operate, secure, support, and scale the service.

Optional product-improvement telemetry is separate and should only be shared if you choose to turn it on.

## Information we do not collect for analytics

LeftLevel metrics must not include:

- message content;
- contact names;
- friend names;
- phone numbers;
- email addresses from message content;
- URLs or hostnames from messages;
- IP addresses tied to users;
- device IDs;
- advertising IDs;
- install IDs;
- session IDs;
- precise location;
- filenames;
- attachment hashes;
- safety numbers;
- peer fingerprints;
- clipboard contents.

## Mandatory service metrics

We collect limited aggregate service metrics that are necessary to operate, secure, support, and scale the service.

These may include:

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

These metrics are aggregate operations counters. They are not intended to identify who you are, who you talk to, or what you say.

## Optional product-improvement telemetry

Optional product-improvement telemetry helps us understand whether the product is easy to use.

If enabled, it may include aggregate counters such as:

- app opened;
- encrypted store created;
- friends added;
- verified, unverified, and changed friend counts;
- links inspected count;
- link warning count;
- link open dismissed count;
- verification confirmed count;
- verification cancelled count.

Optional product-improvement telemetry should be off unless you choose to turn it on.

## Link and attachment safety

LeftLevel may count aggregate safety events, such as blocked-link counts or blocked-attachment counts, to detect abuse and improve protection.

These counts must not include the actual URL, hostname, filename, file hash, message content, or sender/recipient identity.

## Data use

We use permitted metrics to:

- operate the service;
- estimate infrastructure needs;
- detect outages;
- improve reliability;
- prevent abuse;
- understand whether safety features are working;
- improve the app when optional telemetry is enabled.

We do not use essential service metrics or optional product telemetry for advertising, cross-app tracking, data broker sharing, or inferring private social graphs.

## Retention placeholder

Retention periods must be reviewed and finalized before production.

Draft direction:

- keep aggregate service metrics only as long as needed for operations, security, and reliability;
- delete or aggregate further when detailed counters are no longer needed;
- do not retain raw event logs for product analytics.

## Legal review checklist

Before production release, legal review must confirm:

- mandatory service metrics are properly disclosed;
- optional telemetry consent language is correct;
- retention periods are correct;
- regional privacy requirements are covered;
- app store disclosures are accurate;
- no forbidden data appears in metrics payloads;
- user settings accurately reflect what is collected and what is optional.
