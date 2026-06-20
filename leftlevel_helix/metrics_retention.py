from __future__ import annotations

from dataclasses import asdict, dataclass

METRICS_RETENTION_POLICY_VERSION = "LLH-METRICS-RETENTION-v0.1"

RETENTION_LIMITS_DAYS = {
    "essential_service_aggregate": 730,
    "optional_product_aggregate": 365,
    "security_abuse_aggregate": 1095,
    "local_only_user_visible": 0,
}

RAW_EVENT_LOG_RETENTION_DAYS = 0

FORBIDDEN_RETENTION_FIELDS = {
    "message_body",
    "message_text",
    "contact_name",
    "friend_name",
    "url",
    "host",
    "ip_address",
    "device_id",
    "advertising_id",
    "install_id",
    "session_id",
    "filename",
    "attachment_hash",
    "safety_number",
    "peer_fingerprint",
    "precise_location",
}


@dataclass(frozen=True)
class MetricsRetentionRule:
    category: str
    retention_days: int
    aggregate_only: bool = True
    raw_event_logs_allowed: bool = False
    legal_review_required: bool = True

    def __post_init__(self) -> None:
        validate_retention_rule(self)

    def to_dict(self) -> dict[str, object]:
        return {"v": METRICS_RETENTION_POLICY_VERSION, **asdict(self)}


def default_retention_rules() -> list[MetricsRetentionRule]:
    return [
        MetricsRetentionRule("essential_service_aggregate", 730),
        MetricsRetentionRule("optional_product_aggregate", 365),
        MetricsRetentionRule("security_abuse_aggregate", 1095),
        MetricsRetentionRule("local_only_user_visible", 0),
    ]


def validate_retention_rule(rule: MetricsRetentionRule) -> None:
    if rule.category not in RETENTION_LIMITS_DAYS:
        raise ValueError(f"unsupported metrics retention category: {rule.category}")
    if rule.retention_days < 0:
        raise ValueError("retention_days must be non-negative")
    if rule.retention_days > RETENTION_LIMITS_DAYS[rule.category]:
        raise ValueError("retention_days exceeds category maximum")
    if not rule.aggregate_only:
        raise ValueError("metrics retention rules must be aggregate-only")
    if rule.raw_event_logs_allowed:
        raise ValueError("raw event logs are not allowed for metrics retention")
    if not rule.legal_review_required:
        raise ValueError("metrics retention policy requires legal review before production")


def validate_retained_payload(payload: dict[str, object]) -> None:
    serialized_keys = {str(key).lower() for key in payload.keys()}
    for key in serialized_keys:
        if key in FORBIDDEN_RETENTION_FIELDS:
            raise ValueError(f"forbidden retained metrics field: {key}")
        if any(fragment in key for fragment in ("message", "contact", "friend", "url", "host", "ip", "device", "session", "install", "filename", "safety", "fingerprint", "location")):
            raise ValueError(f"forbidden retained metrics field: {key}")


def metrics_retention_policy() -> dict[str, object]:
    return {
        "v": METRICS_RETENTION_POLICY_VERSION,
        "raw_event_log_retention_days": RAW_EVENT_LOG_RETENTION_DAYS,
        "retention_limits_days": dict(RETENTION_LIMITS_DAYS),
        "forbidden_retention_fields": sorted(FORBIDDEN_RETENTION_FIELDS),
        "rules": [
            "retain aggregate metrics only",
            "do not retain raw event logs for product analytics",
            "do not retain message content, contact names, URLs, filenames, safety numbers, fingerprints, or device identifiers",
            "local-only user-visible counters are stored only in the local encrypted store and are not uploaded",
            "legal review is required before production retention periods are finalized",
        ],
    }
