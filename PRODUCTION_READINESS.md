# Production Readiness Plan

LeftLevel Helix should not be launched as a security product until it passes staged gates. Each gate should produce artifacts that can be reviewed by outside experts.

## Gate 1: Prototype correctness

Status in v0.2: partially complete.

Evidence:

- Automated unit tests pass.
- Relay cannot decrypt message envelopes.
- Tampering and replay tests pass.
- Session persistence works.
- Out-of-order delivery works within a bounded window.

Remaining:

- Add property tests.
- Add fuzz tests.
- Add deterministic protocol test vectors.
- Add negative tests for malformed inputs.

## Gate 2: Product architecture

Needed:

- Decide first platform: desktop, Android, iOS, or web.
- Decide relay model: default LeftLevel relay, self-hosted relay, or multi-relay from day one.
- Decide identity recovery model.
- Decide whether message history sync is supported.
- Decide initial group-size target.

## Gate 3: Production implementation

Recommended direction:

- Rust protocol core.
- Mobile bindings through UniFFI or similar.
- Tauri or native desktop wrapper for early testing.
- OS keychain/keystore for local key wrapping.
- Encrypted SQLite for local message storage.

## Gate 4: Endpoint leakage reduction

Needed features:

- No plaintext notification previews by default.
- Screenshot/screen recording blocking where OS supports it.
- Clipboard avoidance.
- Secure compose mode.
- Biometric/app passcode lock.
- Local auto-lock timer.
- Device-compromise warnings.

## Gate 5: Metadata protection

Needed features:

- Multi-relay delivery.
- Optional Tor/I2P support.
- Mailbox padding.
- Message size padding profiles.
- Optional timing jitter.
- Short relay TTLs.
- No IP/content logs by deployment policy.

## Gate 6: Independent review

Required before broad release:

- External cryptographer review.
- Application security audit.
- Mobile security review against OWASP MASVS.
- Infrastructure review.
- Public vulnerability disclosure policy.

## Gate 7: Public beta

Only after the above:

- Public protocol spec.
- Clear security claims.
- Clear non-goals.
- Crash reporting that never captures plaintext.
- Telemetry off by default or privacy-preserving.
- User education for endpoint limits.
