# Contributing to LeftLevel Helix

Thank you for helping build LeftLevel Helix.

LeftLevel is currently a research prototype moving toward a usable product. Contributions are welcome, but security-sensitive changes must be reviewed carefully.

## Current project priorities

1. Make the two-person product workflow reliable.
2. Keep documentation clear and honest.
3. Improve tests before adding complexity.
4. Avoid new integrations until the core app is stable.
5. Preserve the server-blind privacy model.

## Good first contributions

- Documentation improvements.
- Test coverage.
- CLI usability improvements.
- Error-message improvements.
- Local app-store improvements.
- Website copy based on docs.
- Diagrams that explain the protocol.

## Changes that need extra review

Open an issue before starting work on:

- cryptographic primitives;
- key derivation;
- safety-number verification;
- relay protocol changes;
- local secret storage;
- authentication or trust-state behavior;
- dependency changes;
- network privacy or routing changes;
- license or governance changes.

## Development setup

```bash
python -m pip install -e '.[dev]'
pytest -q
```

For real ML-KEM handshakes, install or use OpenSSL 3.5+ with ML-KEM-768 support. GitHub Actions treats the real ML-KEM provider test as environment-dependent.

## Pull request checklist

Before opening a pull request:

- Run `pytest -q`.
- Update documentation if behavior changes.
- Add tests for new behavior.
- Do not include generated vaults, invites, responses, envelopes, or local secret files.
- Do not weaken security warnings or production-readiness disclaimers.
- Do not claim production security without review.

## Contribution licensing

Unless otherwise stated in a separate written agreement, contributions submitted to this repository are intended to be licensed under the repository license in effect at the time the contribution is submitted.

See `docs/LICENSING_AND_COMMERCIAL_MODEL.md` for the current licensing discussion and commercial model options.

## Code of conduct

Be respectful, patient, and security-minded. Assume good intent, but do not ignore risks. Privacy and security projects need clear feedback without personal attacks.
