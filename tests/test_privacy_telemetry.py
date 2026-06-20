from __future__ import annotations

import pytest

from leftlevel_helix.privacy_metrics import MetricsBatch
from leftlevel_helix.privacy_telemetry import (
    PRIVACY_TELEMETRY_EXPORT_VERSION,
    prepare_telemetry_export,
    telemetry_export_policy,
)


def test_prepare_telemetry_export_requires_user_consent():
    batch = MetricsBatch(counters={"messages_sent": 3}, opt_in=True)
    with pytest.raises(ValueError, match="explicit user consent"):
        prepare_telemetry_export(batch, user_consented=False, aggregation_group_size=100)


def test_prepare_telemetry_export_requires_batch_opt_in():
    batch = MetricsBatch(counters={"messages_sent": 3}, opt_in=False)
    with pytest.raises(ValueError, match="marked opt-in"):
        prepare_telemetry_export(batch, user_consented=True, aggregation_group_size=100)


def test_prepare_telemetry_export_requires_minimum_group_size():
    batch = MetricsBatch(counters={"messages_sent": 3}, opt_in=True, min_group_size=100)
    with pytest.raises(ValueError, match="aggregation group size"):
        prepare_telemetry_export(batch, user_consented=True, aggregation_group_size=99)


def test_prepare_telemetry_export_rejects_url_like_destination():
    batch = MetricsBatch(counters={"messages_sent": 3}, opt_in=True)
    with pytest.raises(ValueError, match="not a URL or identifier"):
        prepare_telemetry_export(batch, user_consented=True, aggregation_group_size=100, destination="https://metrics.example.com")


def test_prepare_telemetry_export_rejects_sensitive_destination_terms():
    batch = MetricsBatch(counters={"messages_sent": 3}, opt_in=True)
    with pytest.raises(ValueError, match="sensitive identifier terms"):
        prepare_telemetry_export(batch, user_consented=True, aggregation_group_size=100, destination="device-health")


def test_prepare_telemetry_export_uses_metrics_contract():
    with pytest.raises(ValueError, match="forbidden privacy-sensitive counter"):
        MetricsBatch(counters={"message_body": 1}, opt_in=True)


def test_prepare_telemetry_export_returns_ready_envelope_without_network_io():
    batch = MetricsBatch(
        counters={"messages_sent": 3, "messages_received": 2, "link_open_dismissed": 1},
        dimensions={"platform_family": "desktop", "release_channel": "dev"},
        opt_in=True,
    )

    envelope = prepare_telemetry_export(batch, user_consented=True, aggregation_group_size=150)
    payload = envelope.to_dict()

    assert payload["v"] == PRIVACY_TELEMETRY_EXPORT_VERSION
    assert payload["status"] == "ready_to_export"
    assert payload["destination"] == "leftlevel-product-health"
    assert payload["aggregation_group_size"] == 150
    assert payload["metrics"]["counters"] == {
        "messages_sent": 3,
        "messages_received": 2,
        "link_open_dismissed": 1,
    }
    serialized = repr(payload)
    assert "message_body" not in serialized
    assert "contact_name" not in serialized
    assert "https://" not in serialized
    assert "device_id" not in serialized


def test_telemetry_export_policy_makes_network_io_forbidden():
    policy = telemetry_export_policy()
    assert policy["network_io"] == "forbidden in this module"
    assert policy["requires_user_consent"] is True
    assert policy["requires_batch_opt_in"] is True
    assert policy["requires_minimum_group_size"] is True
    assert "product label only" in policy["destination_rule"]
