from __future__ import annotations

from pathlib import Path

from scripts.scan_for_secrets import scan_path


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_secret_scan_allows_safe_placeholders(tmp_path):
    write(tmp_path / "docs" / "example.md", "Use REPLACE_WITH_SECRET_FROM_SECRET_MANAGER and example.invalid only.\n")

    assert scan_path(tmp_path) == []


def test_secret_scan_blocks_env_files(tmp_path):
    write(tmp_path / ".env", "PLACEHOLDER=value\n")

    findings = scan_path(tmp_path)

    assert findings
    assert findings[0].rule == "forbidden_file"


def test_secret_scan_blocks_vault_files(tmp_path):
    write(tmp_path / "leftlevel-app.llh.vault", "not real vault data\n")

    findings = scan_path(tmp_path)

    assert findings
    assert findings[0].rule == "forbidden_file_type"


def test_secret_scan_blocks_private_key_blocks(tmp_path):
    write(tmp_path / "notes.md", "-----BEGIN PRIVATE KEY-----\nplaceholder\n")

    findings = scan_path(tmp_path)

    assert any(finding.rule == "private_key_block" for finding in findings)


def test_secret_scan_blocks_secret_assignments(tmp_path):
    write(tmp_path / "config.txt", "database_password=super-secret-value\n")

    findings = scan_path(tmp_path)

    assert any(finding.rule == "secret_assignment" for finding in findings)


def test_secret_scan_excludes_scanner_test_fixtures(tmp_path):
    write(tmp_path / "test_secret_scan.py", "database_password=super-secret-value\n")

    findings = scan_path(tmp_path)

    assert findings == []
