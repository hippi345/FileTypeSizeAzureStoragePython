# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 2.x     | Yes       |

## Reporting a vulnerability

If you discover a security issue, please **do not** open a public GitHub issue with sensitive details.

1. Open a private security advisory on GitHub for this repository, or contact the repository owner directly.
2. Include steps to reproduce, impact, and any suggested fix.

## Secrets and credentials

- Never commit storage account keys, connection strings, or SAS tokens to the repository.
- Configure credentials via environment variables (`AZURE_STORAGE_ACCOUNT_NAME`, `AZURE_STORAGE_ACCOUNT_KEY`) or a local `.env` file that is listed in `.gitignore`.
- Rotate any credential that may have been exposed in git history or logs.

## Dependencies

Dependency updates are managed via Dependabot. Keep `azure-storage-blob` and other packages current to receive security fixes from upstream.
