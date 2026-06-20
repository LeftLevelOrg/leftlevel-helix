# Secret Scan Policy

LeftLevel repositories must not contain secrets, credentials, private keys, local encrypted app stores, or deployment-specific sensitive artifacts.

## Product rule

Never commit secrets.

Never commit AWS credentials or deployment credentials.

Never commit local encrypted app stores.

Use placeholders and secret managers instead of real values.

## Secret scanner

The repository secret scanner lives at:

```bash
python scripts/scan_for_secrets.py
```

The scanner checks for:

- forbidden environment files;
- local encrypted app store files;
- private key files;
- private certificate/key file types;
- obvious cloud access key patterns;
- private key blocks;
- common token patterns;
- secret assignment patterns such as passwords, API keys, session tokens, and webhook secrets.

## Safe placeholders

The scanner allows safe placeholders such as:

- `REPLACE_WITH_SECRET_FROM_SECRET_MANAGER`
- `AWS_ACCOUNT_ID_REDACTED`
- `AWS_REGION_EXAMPLE`
- `example.invalid`

## Required gate

Release readiness validation must run the secret scanner.

A release candidate must fail if the scanner finds possible secret material.

## If a secret is found

If secret material is found:

1. Stop release work.
2. Treat the value as compromised.
3. Rotate or revoke the secret.
4. Remove the secret from the repository and history if necessary.
5. Review logs, AWS usage, and billing.
6. Add a test or policy update to prevent recurrence.

## Limitations

Automated scanning is a safety net, not a guarantee.

Manual review, GitHub secret scanning, branch protection, least-privilege deployment access, and AWS billing alarms are still required.
