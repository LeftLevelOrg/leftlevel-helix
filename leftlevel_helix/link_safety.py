from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass, asdict
from urllib.parse import urlsplit, urlunsplit

LINK_SAFETY_VERSION = "LLH-LINK-SAFETY-v0.1"

URL_PATTERN = re.compile(r"(?i)\b((?:[a-z][a-z0-9+.-]*):(?://)?[^\s<>'\"]+)")
TRAILING_PUNCTUATION = ".,;:!?)]]}>'\""
ALLOWED_REVIEW_SCHEMES = {"http", "https"}
BLOCKED_SCHEMES = {"javascript", "data", "file", "ftp", "smb", "ssh", "tel", "mailto"}


@dataclass(frozen=True)
class LinkFinding:
    raw_url: str
    normalized_url: str
    scheme: str
    host: str
    verdict: str
    reasons: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def extract_urls(text: str) -> list[str]:
    urls: list[str] = []
    for match in URL_PATTERN.finditer(text):
        raw = match.group(1).rstrip(TRAILING_PUNCTUATION)
        if raw:
            urls.append(raw)
    return urls


def analyze_links(text: str) -> list[LinkFinding]:
    return [analyze_url(url) for url in extract_urls(text)]


def analyze_url(raw_url: str) -> LinkFinding:
    parsed = urlsplit(raw_url.strip())
    scheme = parsed.scheme.lower()
    host = parsed.hostname or ""
    reasons: list[str] = []
    verdict = "review"

    if not scheme:
        return _finding(raw_url, parsed, scheme, host, "blocked", ["missing URL scheme"])

    if scheme in BLOCKED_SCHEMES or scheme not in ALLOWED_REVIEW_SCHEMES:
        return _finding(raw_url, parsed, scheme, host, "blocked", [f"blocked URL scheme: {scheme}"])

    if scheme == "http":
        reasons.append("plain HTTP link")

    if parsed.username or parsed.password:
        reasons.append("URL contains username or password text before the host")

    if not host:
        return _finding(raw_url, parsed, scheme, host, "blocked", ["missing URL host"])

    if _is_private_or_local_host(host):
        return _finding(raw_url, parsed, scheme, host, "blocked", ["local or private network target"])

    if _needs_idn_review(host):
        reasons.append("internationalized or punycode hostname needs review")

    if _looks_like_ip_literal(host):
        reasons.append("IP address link needs review")

    if _looks_like_single_label_host(host):
        reasons.append("single-label hostname needs review")

    if reasons:
        verdict = "warning"

    return _finding(raw_url, parsed, scheme, host, verdict, reasons or ["no obvious local parsing risk found"])


def _finding(raw_url, parsed, scheme: str, host: str, verdict: str, reasons: list[str]) -> LinkFinding:
    normalized_host = _idna_ascii(host).lower() if host else ""
    netloc = normalized_host
    if parsed.port:
        netloc = f"{netloc}:{parsed.port}"
    normalized_url = urlunsplit((scheme, netloc, parsed.path or "", parsed.query or "", ""))
    return LinkFinding(
        raw_url=raw_url,
        normalized_url=normalized_url,
        scheme=scheme,
        host=host,
        verdict=verdict,
        reasons=reasons,
    )


def _idna_ascii(host: str) -> str:
    try:
        return host.encode("idna").decode("ascii")
    except UnicodeError:
        return host


def _needs_idn_review(host: str) -> bool:
    ascii_host = _idna_ascii(host)
    return host != ascii_host or "xn--" in ascii_host.lower()


def _looks_like_ip_literal(host: str) -> bool:
    try:
        ipaddress.ip_address(host.strip("[]"))
        return True
    except ValueError:
        return False


def _looks_like_single_label_host(host: str) -> bool:
    return "." not in host and not _looks_like_ip_literal(host)


def _is_private_or_local_host(host: str) -> bool:
    normalized = host.strip("[]").lower().rstrip(".")
    if normalized in {"localhost", "0", "0.0.0.0"}:
        return True
    if normalized.endswith(".local") or normalized.endswith(".localhost"):
        return True
    try:
        ip = ipaddress.ip_address(normalized)
    except ValueError:
        return False
    return any(
        [
            ip.is_private,
            ip.is_loopback,
            ip.is_link_local,
            ip.is_multicast,
            ip.is_reserved,
            ip.is_unspecified,
        ]
    )
