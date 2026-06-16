from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

PRIVACY_METRICS_CONTRACT_VERSION = "LLH-PRIVACY-METRICS-v0.1"

ALLOWED_COUNTERS = {
    "app_opened",
    "store_created",
    "friends_added",
    "verified_friends",
    "unverified_friends",
    "changed_friends",
    "messages_sent",
    "messages_received",
    "links_inspected",
    "links_blocked",
    "links_warning",
    "link_open_dismissed",
    "link_open_confirmed",
    "attachments_queued",
    "attachments_blocked",
    "attachment_preview_dismissed",
    "send_blocked_changed_friend",
    "send_warning_dismissed",
    "verify_confirmed",
    "verify_cancelled",
    "errors_total",
}

ALLOWED_DIMENSIONS = {
    "app_version",
    "platform_family",
    "release_channel",
    "locale_language",
    "consent_mode",
}

FORBIDDEN_KEYS = {
    "message",
    "message_body",
    "body",
    "text",
    "contact",
    "contact_name",
    "friend_name",
    "phone",
    "email",
    "url",
    "raw_url",
    "host",
    "ip",
    "ip_address",
    "device_id",
    "advertising_id",
    "install_id",
    "session_id",
    "location",
    "latitude",
    "longitude",
    "file_name",
    "filename",
    "attachment_hash",
    "safety_number",
    "safety_short_code",
    "peer_fingerprint",
    "clipboard",
}

FORBIDDEN_KEY_FRAGMENTS = {
    "message",
    "contact",
    "friend",
    "phone",
    "email",
    "url",
    "host",
    "ip",
    "device",
    "advertising",
    "install",
    "session",
    "location",
    "latitude",
    "longitude",
    "file",
    "attachment_hash",
    "safety",
    "fingerprint",
    "clipboard",
}


@dataclass(frozen=True)
class MetricsBatch:
    counters: dict[str, int]
    dimensions: dict[str, str] = field(default_factory=dict)
    min_group_size: int = 100
    opt_in: bool = False

    def __post_init__(self) -> None:
        validate_metrics_batch(self)

    def to_dict(self) -> dict[str, object]:
        return {"v": PRIVACY_METRICS_CONTRACT_VERSION, **asdict(self)}


def empty_metrics_batch(*, opt_in: bool = False) -> MetricsBatch:
    return MetricsBatch(counters={}, dimensions={}, opt_in=opt_in)


def increment_counter(batch: MetricsBatch, counter: str, amount: int = 1) -> MetricsBatch:
    if amount < 0:
        raise ValueError("metrics counters cannot be decremented")
    counters = dict(batch.counters)
    counters[counter] = counters.get(counter, 0) + amount
    return MetricsBatch(counters=counters, dimensions=dict(batch.dimensions), min_group_size=batch.min_group_size, opt_in=batch.opt_in)


def local_app_store_metrics(state: dict[str, Any], *, opt_in: bool = False) -> MetricsBatch:
    contacts = state.get("contacts", {})
    messages = state.get("messages", [])
    counters = {
        "friends_added": len(contacts),
        "verified_friends": sum(1 for item in contacts.values() if item.get("trust_state") == "verified"),
        "unverified_friends": sum(1 for item in contacts.values() if item.get("trust_state") == "unverified"),
        "changed_friends": sum(1 for item in contacts.values() if item.get("trust_state") == "changed"),
        "messages_sent": sum(1 for item in messages if item.get("direction") == "sent"),
        "messages_received": sum(1 for item in messages if item.get("direction") == "received"),
    }
    return MetricsBatch(counters=counters, dimensions={}, opt_in=opt_in)


def validate_metrics_batch(batch: MetricsBatch) -> None:
    if batch.min_group_size < 100:
        raise ValueError("min_group_size must be at least 100")
    for name, value in batch.counters.items():
        _validate_metric_key(name, allowed=ALLOWED_COUNTERS, label="counter")
        if not isinstance(value, int) or value < 0:
            raise ValueError("metrics counter values must be non-negative integers")
    for name, value in batch.dimensions.items():
        _validate_metric_key(name, allowed=ALLOWED_DIMENSIONS, label="dimension")
        if not isinstance(value, str) or len(value) > 64:
            raise ValueError("metrics dimensions must be short strings")
        _validate_metric_value(value)


def _validate_metric_key(name: str, *, allowed: set[str], label: str) -> None:
    normalized = name.lower()
    if normalized in FORBIDDEN_KEYS:
        raise ValueError(f"forbidden privacy-sensitive {label}: {name}")
    if any(fragment in normalized for fragment in FORBIDDEN_KEY_FRAGMENTS):
        raise ValueError(f"forbidden privacy-sensitive {label}: {name}")
    if name not in allowed:
        raise ValueError(f"unsupported metrics {label}: {name}")


def _validate_metric_value(value: str) -> None:
    lowered = value.lower()
    if "://" in lowered or "@" in lowered:
        raise ValueError("metrics dimensions must not contain URLs or identifiers")
    if any(fragment in lowered for fragment in ("http", "mailto", "tel:", "file:", "data:")):
        raise ValueError("metrics dimensions must not contain URL-like values")


def metrics_contract() -> dict[str, object]:
    return {
        "v": PRIVACY_METRICS_CONTRACT_VERSION,
        "allowed_counters": sorted(ALLOWED_COUNTERS),
        "allowed_dimensions": sorted(ALLOWED_DIMENSIONS),
        "forbidden_keys": sorted(FORBIDDEN_KEYS),
        "rules": [
            "metrics are opt-in for telemetry export",
            "local-only counters may be shown to the user",
            "do not collect message content",
            "do not collect contact names or identifiers",
            "do not collect URLs, hosts, IP addresses, or filenames",
            "do not collect device IDs, advertising IDs, install IDs, or session IDs",
            "use aggregate counters with minimum group size before remote reporting",
        ],
    }
