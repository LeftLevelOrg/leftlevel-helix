from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime

from .privacy_metrics import MetricsBatch, validate_metrics_batch

PRIVACY_TELEMETRY_EXPORT_VERSION = "LLH-PRIVACY-TELEMETRY-EXPORT-v0.1"


@dataclass(frozen=True)
class TelemetryExportEnvelope:
    status: str
    destination: str
    aggregation_group_size: int
    created_at: str
    metrics: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {"v": PRIVACY_TELEMETRY_EXPORT_VERSION, **asdict(self)}


def prepare_telemetry_export(
    batch: MetricsBatch,
    *,
    user_consented: bool,
    aggregation_group_size: int,
    destination: str = "leftlevel-product-health",
) -> TelemetryExportEnvelope:
    """Prepare a privacy-preserving telemetry payload without sending it.

    This function intentionally performs no network I/O. A future uploader must call
    this first and must send only the returned envelope.
    """
    if not user_consented:
        raise ValueError("telemetry export requires explicit user consent")
    if not batch.opt_in:
        raise ValueError("metrics batch must be marked opt-in before export")
    validate_metrics_batch(batch)
    if aggregation_group_size < batch.min_group_size:
        raise ValueError("telemetry export requires aggregation group size to meet the minimum")
    _validate_destination(destination)
    return TelemetryExportEnvelope(
        status="ready_to_export",
        destination=destination,
        aggregation_group_size=aggregation_group_size,
        created_at=datetime.now(UTC).replace(microsecond=0).isoformat(),
        metrics=batch.to_dict(),
    )


def _validate_destination(destination: str) -> None:
    if not destination:
        raise ValueError("telemetry destination is required")
    lowered = destination.lower()
    if "://" in lowered or "@" in lowered:
        raise ValueError("telemetry destination must be a product label, not a URL or identifier")
    if any(fragment in lowered for fragment in ("url", "host", "ip", "device", "session", "install", "email")):
        raise ValueError("telemetry destination label must not contain sensitive identifier terms")


def telemetry_export_policy() -> dict[str, object]:
    return {
        "v": PRIVACY_TELEMETRY_EXPORT_VERSION,
        "network_io": "forbidden in this module",
        "requires_user_consent": True,
        "requires_batch_opt_in": True,
        "requires_minimum_group_size": True,
        "destination_rule": "product label only; no URL, host, IP, device, install, session, or email identifier",
        "payload_rule": "export only privacy_metrics.MetricsBatch data that passes the metrics contract",
    }
