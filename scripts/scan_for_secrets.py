from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

SECRET_SCAN_VERSION = "LLH-SECRET-SCAN-v0.1"

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
}

EXCLUDED_FILE_NAMES = {
    "scan_for_secrets.py",
    "test_secret_scan.py",
}

FORBIDDEN_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_ed25519",
}

FORBIDDEN_SUFFIXES = {
    ".llh.vault",
    ".pem",
    ".p12",
    ".pfx",
    ".key",
}

SAFE_PLACEHOLDERS = {
    "REPLACE_WITH_SECRET_FROM_SECRET_MANAGER",
    "AWS_ACCOUNT_ID_REDACTED",
    "AWS_REGION_EXAMPLE",
    "example.invalid",
}

PATTERNS = {
    "aws_access_key_id": re.compile(r"\b(A3T[A-Z0-9]|AKIA|ASIA)[A-Z0-9]{16}\b"),
    "private_key_block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "secret_assignment": re.compile(
        r"(?i)\b(aws_secret_access_key|secret_access_key|session_token|api_key|private_key|webhook_secret|database_password|password)\s*=\s*([^\s#]+)"
    ),
}

TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
}


@dataclass(frozen=True)
class SecretFinding:
    path: str
    rule: str
    line: int
    detail: str

    def format(self) -> str:
        return f"{self.path}:{self.line}: {self.rule}: {self.detail}"


def scan_path(root: Path) -> list[SecretFinding]:
    findings: list[SecretFinding] = []
    for path in sorted(root.rglob("*")):
        if _is_excluded(path):
            continue
        if path.is_file():
            findings.extend(_scan_file(root, path))
    return findings


def _is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def _scan_file(root: Path, path: Path) -> list[SecretFinding]:
    relative = path.relative_to(root).as_posix()
    findings: list[SecretFinding] = []

    if path.name in FORBIDDEN_FILE_NAMES:
        findings.append(SecretFinding(relative, "forbidden_file", 1, "real environment or private key file must not be committed"))
    if path.suffix in FORBIDDEN_SUFFIXES:
        findings.append(SecretFinding(relative, "forbidden_file_type", 1, "sensitive file type must not be committed"))
    if path.name in EXCLUDED_FILE_NAMES:
        return findings
    if path.suffix not in TEXT_SUFFIXES:
        return findings

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings

    for line_number, line in enumerate(text.splitlines(), start=1):
        if _line_is_safe_placeholder(line):
            continue
        for rule, pattern in PATTERNS.items():
            match = pattern.search(line)
            if match:
                detail = "potential secret or credential material"
                findings.append(SecretFinding(relative, rule, line_number, detail))
    return findings


def _line_is_safe_placeholder(line: str) -> bool:
    return any(placeholder in line for placeholder in SAFE_PLACEHOLDERS)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan repository files for obvious committed secrets.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    findings = scan_path(Path(args.root).resolve())
    if findings:
        print(f"{SECRET_SCAN_VERSION} failed")
        for finding in findings:
            print(f"- {finding.format()}")
        return 1
    print(f"{SECRET_SCAN_VERSION} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
