from __future__ import annotations

from dataclasses import asdict, dataclass, field
from uuid import uuid4

URL_VALIDATION_WORKER_CONTRACT_VERSION = "LLH-URL-VALIDATION-WORKER-v0.1"
ALLOWED_WORKER_VERDICTS = {"blocked", "warning", "no_obvious_risk_found", "error"}
FORBIDDEN_WORKER_VERDICTS = {"safe", "trusted", "verified_safe"}


@dataclass(frozen=True)
class UrlValidationRequest:
    request_id: str
    url: str
    timeout_seconds: int = 15
    max_redirects: int = 3
    max_response_bytes: int = 1_000_000

    def to_dict(self) -> dict[str, object]:
        return {"v": URL_VALIDATION_WORKER_CONTRACT_VERSION, **asdict(self)}


@dataclass(frozen=True)
class UrlValidationResult:
    request_id: str
    original_url: str
    verdict: str
    reasons: list[str]
    final_url: str | None = None
    redirect_chain: list[str] = field(default_factory=list)
    observed_mime_type: str | None = None
    downloaded_bytes: int = 0
    network_used: bool = False
    timed_out: bool = False

    def __post_init__(self) -> None:
        if self.verdict not in ALLOWED_WORKER_VERDICTS:
            raise ValueError(f"unsupported URL validation verdict: {self.verdict}")
        if self.verdict in FORBIDDEN_WORKER_VERDICTS:
            raise ValueError("URL validation worker must not claim a URL is safe")

    def to_dict(self) -> dict[str, object]:
        return {"v": URL_VALIDATION_WORKER_CONTRACT_VERSION, **asdict(self)}


def make_validation_request(url: str, *, timeout_seconds: int = 15) -> UrlValidationRequest:
    if timeout_seconds <= 0 or timeout_seconds > 60:
        raise ValueError("timeout_seconds must be between 1 and 60")
    return UrlValidationRequest(request_id=uuid4().hex, url=url, timeout_seconds=timeout_seconds)


def worker_isolation_requirements() -> list[str]:
    return [
        "no vault access",
        "no contacts access",
        "no message history access",
        "no user cookies",
        "no user browser profile",
        "no local-network access",
        "no platform secrets",
        "temporary scratch filesystem only",
        "short execution timeout",
        "fresh worker identity for each scan",
        "separate process or sandbox boundary",
        "no message renderer access",
    ]


def worker_contract() -> dict[str, object]:
    return {
        "v": URL_VALIDATION_WORKER_CONTRACT_VERSION,
        "allowed_verdicts": sorted(ALLOWED_WORKER_VERDICTS),
        "forbidden_verdicts": sorted(FORBIDDEN_WORKER_VERDICTS),
        "isolation_requirements": worker_isolation_requirements(),
        "result_rule": "return blocked, warning, no_obvious_risk_found, or error; never return safe",
    }
