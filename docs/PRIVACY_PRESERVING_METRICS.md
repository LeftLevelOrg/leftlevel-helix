# Privacy-Preserving Metrics

LeftLevel needs enough product telemetry to run a successful app, but metrics must not compromise privacy or security.

The product rule is simple: count product health, never collect content or identity.

## Current status

Current implementation:

- privacy metrics contract exists;
- local aggregate counters can be produced from the encrypted app store;
- sensitive field names are blocked by tests;
- remote telemetry upload is not implemented yet.

## Allowed metrics

Allowed counters include aggregate counts such as:

- app opened;
- encrypted store created;
- friends added;
- verified, unverified, and changed friend counts;
- messages sent count;
- messages received count;
- links inspected count;
- links blocked count;
- link warnings count;
- link open dismissed count;
- attachment blocked count;
- send blocked because friend state changed;
- verification confirmed count;
- verification cancelled count;
- aggregate error count.

These counters are useful for product health and safety decisions without exposing user content.

## Forbidden data

Metrics must not collect:

- message content;
- contact names;
- phone numbers;
- email addresses;
- URLs;
- hostnames;
- IP addresses;
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

Remote telemetry should be opt-in.

Local-only counters may be shown to the user without uploading them.

The app should clearly explain what is counted and what is never collected.

## Aggregation rules

Remote reporting should use aggregated counters only.

Minimum group size should be at least 100 before reporting product-level metrics.

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
- are errors increasing after a release.

It should not answer:

- who someone talks to;
- what someone says;
- what links someone receives;
- where someone is;
- which exact device or person is using the app.

## Product promise

LeftLevel can measure whether the product works without measuring the private lives of the people using it.
