from __future__ import annotations

from dataclasses import asdict, dataclass, field

ESSENTIAL_SERVICE_METRICS_VERSION = "LLH-ESSENTIAL-SERVICE-METRICS-v0.1"

ALLOWED_ESSENTIAL_COUNTERS = {
    "registered_users_total",
    "active_users_estimate",
    "messages_sent_total",
    "messages_received_total",
    "relay_envelopes_stored",
    "relay_envelopes_fetched",
    "delivery_failures_total",
    "errors_total",
    "abuse_reports_total",
    "links_blocked_total",
    "attachments_blocked_total",
}

FORBIDDEN_ESSENTIAL_KEYS = {
    "message_body",
    "message_text",
    "contact_name",
    "friend_name",
    "phone",
    "email",
    "url",
    "host",
    "ip_address",
    "device_id",
    "advertising_id",
    "install_id",
    "session_id",
    "precise_location",
    "filename",
    "attachment_hash",
    "safety_number",
    "peer_fingerprint",
}


@dataclass(frozen=True)
class EssentialServiceMetricsReport:
    counters: dict[str, int]
    purpose: str = "service_operations"
    notice_required: bool = True
    opt_in_required: bool = False
    upload_allowed: bool = True
    dimensions: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        validate_essential_service_metrics(self)

    def to_dict(self) -> dict[str, object]:
        return {"v": ESSENTIAL_SERVICE_METRICS_VERSION, **asdict(self)}


def validate_essential_service_metrics(report: EssentialServiceMetricsReport) -> None:
    if report.purpose != "service_operations":
        raise ValueError("essential metrics purpose must be service_operations")
    if not report.notice_required:
        raise ValueError("essential metrics require clear notice")
    if report.opt_in_required:
        raise ValueError("essential service metrics are mandatory disclosed operations metrics, not opt-in telemetry")
    for name, value in report.counters.items():
        if name in FORBIDDEN_ESSENTIAL_KEYS:
            raise ValueError(f"forbidden essential metrics field: {name}")
        if name not in ALLOWED_ESSENTIAL_COUNTERS:
            raise ValueError(f"unsupported essential metrics counter: {name}")
        if not isinstance(value, int) or value < 0:
            raise ValueError("essential metrics counters must be non-negative integers")
    for name, value in report.dimensions.items():
        _validate_dimension(name, value)


def _validate_dimension(name: str, value: str) -> None:
    if name not in {"app_version", "platform_family", "release_channel", "region_bucket"}:
        raise ValueError(f"unsupported essential metrics dimension: {name}")
    lowered = value.lower()
    if any(fragment in lowered for fragment in ("://", "@", "http", "url", "host", "ip", "device", "session", "install")):
        raise ValueError("essential metrics dimensions must not contain identifiers")


def essential_service_metrics_policy() -> dict[str, object]:
    return {
        "v": ESSENTIAL_SERVICE_METRICS_VERSION,
        "status": "mandatory_disclosed_operations_metrics",
        "opt_in_required": False,
        "notice_required": True,
        "allowed_counters": sorted(ALLOWED_ESSENTIAL_COUNTERS),
        "forbidden_fields": sorted(FORBIDDEN_ESSENTIAL_KEYS),
        "rules": [
            "collect only aggregate counters needed to operate and support the service",
            "disclose essential metrics clearly in the privacy notice and terms",
            "do not collect message content or social graph data",
            "do not collect URLs, hostnames, IP addresses, filenames, safety numbers, or device identifiers",
            "do not use essential metrics for advertising, cross-app tracking, or data broker sharing",
        ],
    }
