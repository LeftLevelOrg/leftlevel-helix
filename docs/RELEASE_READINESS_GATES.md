# Release Readiness Gates

LeftLevel Helix should remain labeled as a prototype until the release gates in this document are complete.

## Current status

Current status: prototype and review candidate.

The project is not yet approved for production use.

## Gate 1: protocol readiness

Required before approval:

- current protocol document;
- current security model;
- current protection matrix;
- protocol test vectors;
- replay and tamper tests;
- documented limitations.

## Gate 2: implementation readiness

Required before approval:

- passing unit tests;
- passing integration tests;
- dependency inventory;
- code review for protocol and storage modules;
- compatibility notes for serialized data.

## Gate 3: local storage readiness

Required before approval:

- encrypted app-store tests;
- encrypted attachment-store tests;
- passphrase handling notes;
- backup and recovery notes;
- documented local-device limitations.

## Gate 4: relay readiness

Required before approval:

- relay-visible field review;
- logging policy;
- deployment guidance;
- rate-limit and abuse-handling plan;
- incident response notes.

## Gate 5: user interface readiness

Required before approval:

- contact trust states visible;
- safety-number comparison flow;
- send and receive flow;
- delivery, empty, and failure states;
- attachment integrity states;
- mitigation actions for failed attachment checks.

## Gate 6: release readiness

Required before approval:

- versioning policy;
- changelog;
- signed release artifacts;
- reproducible build plan;
- rollback notes.

## Gate 7: public documentation readiness

Required before approval:

- README status is current;
- website messaging matches repository status;
- limitations are clear;
- security contact process is documented;
- public materials avoid unsupported claims.

## Sign-off record template

```text
Release candidate:
Commit SHA:
Protocol gate:
Implementation gate:
Storage gate:
Relay gate:
User interface gate:
Release gate:
Documentation gate:
Known limitations:
Decision: approved / rejected / deferred
Approvers:
Date:
```

## Blocking conditions

The project must remain marked as not production-ready if any gate is incomplete.
