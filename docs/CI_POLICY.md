# CI Policy

The default CI workflow is intended to provide portable validation for every push and pull request.

## Portable test suite

CI runs:

```bash
python -m pytest -q -m 'not real_mlkem' -ra
```

The real ML-KEM integration test is environment-dependent because it requires an OpenSSL provider with ML-KEM-768 support. That test should be run in environments that provide the required provider.

## Readiness documentation validation

CI also runs:

```bash
python scripts/validate_release_readiness.py
```

This check ensures required release-readiness documents exist and contain key sections.

## Secret scan validation

CI runs the repository secret scan directly:

```bash
python scripts/scan_for_secrets.py
```

Release readiness validation also runs the secret scan.

CI must fail if obvious secret material, forbidden environment files, private key files, local encrypted app stores, or sensitive deployment artifacts are committed.

## Workflow permissions

The CI workflow should use read-only repository contents permission.

The workflow must not require AWS credentials, deployment credentials, or production secrets.

Deployment workflows should be separate from this portable validation workflow and should use least-privilege access with environment approvals.

## Production readiness boundary

Passing CI does not mean the project is production-ready.

Production readiness still requires completion of the release readiness gates and an approved sign-off record.
