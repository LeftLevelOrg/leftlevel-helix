# Cost Model

This document tracks which pieces of the planned LeftLevel stack are free to use and which parts may create real costs later.

## Framework cost

Tauri is free/open-source. The framework itself does not require a license fee from LeftLevel.

The recommended architecture remains:

```text
Tauri v2 app shell
Rust core over time
Web UI
LeftLevel relay protocol
Encrypted local app store
```

## Expected no-cost pieces

| Item | Expected cost | Notes |
|---|---:|---|
| Tauri framework | $0 | Open-source framework. |
| Rust language/toolchain | $0 | Open-source toolchain. |
| Web UI source code | $0 | We can build our own UI. |
| LeftLevel core protocol code | $0 internal license cost | We own/control the project code. |
| Local development builds | $0 | Development can happen locally without app-store publishing. |
| GitHub public repository | $0 for basic public hosting | Extra paid services may be optional later. |

## Costs to expect later

| Item | Expected cost | Why it may matter |
|---|---:|---|
| Apple Developer Program | $99/year | Needed for normal App Store distribution and some Apple distribution workflows. |
| Google Play Console | $25 one-time | Needed to publish through Google Play. |
| Code-signing certificates | Varies | Needed for smoother trusted desktop distribution. |
| Hosted relay servers | Varies | Required if LeftLevel runs official public relays. |
| Security audit | Varies, often significant | Needed before serious production security claims. |
| Domain/hosting/website | Varies | Needed for public product presence. |
| App-store review/support time | Staff time | Not a direct framework fee, but real operational effort. |

## Recommendation

Use free/open-source tooling for the product build. Spend money only where it improves trust, distribution, and reliability:

1. official website and domain;
2. code signing;
3. Apple/Google developer accounts when mobile distribution is ready;
4. hosted relay infrastructure;
5. independent security review.

## Business model fit

Free/open-source tooling still supports a business model:

- open-source core;
- paid hosted relay service;
- paid official builds/support;
- enterprise/private deployments;
- consulting and security review support;
- future commercial integrations.

The framework choice does not prevent LeftLevel from making money.
