# URL Validation Worker Contract

This document defines the contract for a future isolated URL validation worker.

The worker is not a general browser for users. It is a disposable inspection environment for checking hostile links without exposing the main app, vault, contacts, cookies, or local device.

## Current status

Current implementation:

- local link parsing and inspection exists;
- message URLs are rendered as plain text;
- URLs are not made clickable automatically;
- active isolated URL validation is designed but not implemented yet.

## Worker purpose

The URL validation worker may inspect a URL in a disposable environment and return a risk label.

It must not return a guarantee that a URL is safe.

Allowed verdicts:

- `blocked`: do not open;
- `warning`: review first;
- `no_obvious_risk_found`: no obvious risk was found by the worker;
- `error`: the worker could not complete validation.

Forbidden verdicts:

- `safe`;
- `trusted`;
- `verified_safe`.

## Isolation requirements

The worker must run with least privilege.

Required isolation:

- no vault access;
- no contacts access;
- no message history access;
- no user cookies;
- no user browser profile;
- no local-network access;
- no access to platform secrets;
- no host filesystem write access except temporary scratch space;
- short execution timeout;
- fresh worker identity for each scan;
- separate process or sandbox boundary from the main app;
- no access to the message renderer process.

## Network policy

The worker should not have broad network access.

Allowed network behavior:

- connect to the target URL being validated;
- follow redirects only up to a small limit;
- optionally query approved reputation services;
- block private IPs, localhost, link-local addresses, and internal names;
- block disallowed schemes such as `javascript:`, `data:`, `file:`, `smb:`, and `ftp:`.

## Collection limits

The worker may collect:

- redirect chain;
- final URL;
- final host;
- TLS certificate summary;
- MIME type;
- response size up to a configured limit;
- download attempt indicators;
- reputation source labels;
- blocked scheme or blocked network reason.

The worker must not collect:

- user cookies;
- user credentials;
- local files;
- vault contents;
- contact list data;
- full message history.

## Result format

A worker result should include:

- contract version;
- request ID;
- original URL;
- final URL, if reached;
- verdict;
- reasons;
- redirect chain;
- observed MIME type, if known;
- downloaded byte count, if any;
- whether network access was used;
- whether the run timed out.

## Product behavior

The main app should treat worker output as advisory.

Recommended UI behavior:

- `blocked`: red indicator, do not open;
- `warning`: yellow indicator, review first;
- `no_obvious_risk_found`: neutral or yellow indicator, still require deliberate open action;
- `error`: yellow indicator, validation unavailable.

The UI must not say a URL is safe just because the worker did not find a problem.

## Implementation sequence

Recommended sequence:

1. Keep URLs plain text by default.
2. Run local parsing and inspection.
3. Block obvious local risks.
4. Show a review screen.
5. Add isolated worker validation.
6. Add reputation providers.
7. Add external browser handoff only after explicit confirmation.
