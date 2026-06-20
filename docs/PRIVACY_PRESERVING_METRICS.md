# Privacy-Preserving Metrics

LeftLevel needs enough metrics to run a successful app, but metrics must not compromise privacy or security.

The product rule is simple: count product health, never collect content or identity.

## Current status

Current implementation:

- privacy metrics contract exists;
- essential service metrics contract exists;
- local aggregate counters can be produced from the encrypted app store;
- sensitive field names are blocked by tests;
- remote optional telemetry upload is not implemented yet.

## Metric categories

LeftLevel separates metrics into two categories.

### Essential service metrics

Essential service metrics are mandatory disclosed operations metrics.

They are used to operate, secure, support, and scale the service.

Examples:

- registered users total;
- active users estimate;
- messages sent total;
- messages received total;
- delivery failures total;
- aggregate error count;
- abuse reports total;
- links blocked total;
- attachments blocked total.

These do not require opt-in when they are truly necessary to operate the service and are clearly disclosed in the privacy notice and terms.

### Optional product-improvement telemetry

Optional telemetry is used to improve product experience.

Examples:

- app opened;
- encrypted store created;
- friends added;
- verified, unverified, and changed friend counts;
- links inspected count;
- link warnings count;
- link open dismissed count;
- verification confirmed count;
- verification cancelled count.

Optional telemetry should be opt-in for remote export.

Local-only counters may be shown to the user without uploading them.

## Forbidden data

Metrics must not collect:

- message content;
- contact names;
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
- peer fingerprints;
- clipboard contents.

## Dimensions

Allowed dimensions are limited to broad app-operation context:

- app version;
- platform family;
- release channel;
- language;
- consent mode.

Dimensions must be short strings and must not contain identifiers, URLs, or user data.

## Consent model

Essential service metrics may be mandatory when they are necessary to operate the service and clearly disclosed.

Optional product-improvement telemetry should be opt-in for remote export.

Local-only counters may be shown to the user without uploading them.

The app should clearly explain what is counted, why it is counted, whether it is mandatory, and what is never collected.

## Aggregation rules

Remote reporting should use aggregated counters only.

Minimum group size should be at least 100 before reporting product-level optional telemetry.

Essential service metrics should still be aggregate-only and minimized.

Do not upload raw event logs.

Do not upload per-user timelines.

Do not upload stable identifiers that allow cross-context tracking.

## Useful product questions this can answer

This metrics model can answer:

- are people opening the app;
- are users creating encrypted stores successfully;
- are users adding friends successfully;
- are messages being sent and received;
- are users hitting link safety warnings;
- are users dismissing link warnings;
- are attachments being blocked often;
- are verification flows being cancelled;
- are changed-friend safety blocks happening;
- are errors increasing after a release;
- does the service have enough capacity;
- are delivery failures increasing.

It should not answer:

- who someone talks to;
- what someone says;
- what links someone receives;
- where someone is;
- which exact device or person is using the app.

## Product promise

LeftLevel can measure whether the product works without measuring the private lives of the people using it.
