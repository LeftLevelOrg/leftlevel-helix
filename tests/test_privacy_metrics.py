from __future__ import annotations

import pytest

from leftlevel_helix.privacy_metrics import (
    PRIVACY_METRICS_CONTRACT_VERSION,
    MetricsBatch,
    empty_metrics_batch,
    increment_counter,
    local_app_store_metrics,
    metrics_contract,
)


def test_metrics_batch_exports_contract_version():
    batch = MetricsBatch(counters={"messages_sent": 2}, dimensions={"platform_family": "desktop"}, opt_in=True)
    payload = batch.to_dict()
    assert payload["v"] == PRIVACY_METRICS_CONTRACT_VERSION
    assert payload["counters"] == {"messages_sent": 2}
    assert payload["dimensions"] == {"platform_family": "desktop"}
    assert payload["min_group_size"] == 100


def test_increment_counter_only_allows_known_aggregate_counters():
    batch = empty_metrics_batch(opt_in=True)
    updated = increment_counter(batch, "link_open_dismissed")
    assert updated.counters == {"link_open_dismissed": 1}

    with pytest.raises(ValueError, match="unsupported metrics counter"):
        increment_counter(batch, "custom_button_clicked")


def test_metrics_reject_privacy_sensitive_counter_names():
    for key in ["message_body", "contact_name", "url", "ip_address", "device_id", "file_name", "safety_number"]:
        with pytest.raises(ValueError, match="forbidden privacy-sensitive counter"):
            MetricsBatch(counters={key: 1})


def test_metrics_reject_privacy_sensitive_dimension_names_and_values():
    with pytest.raises(ValueError, match="forbidden privacy-sensitive dimension"):
        MetricsBatch(counters={}, dimensions={"device_id": "abc"})
    with pytest.raises(ValueError, match="URLs or identifiers"):
        MetricsBatch(counters={}, dimensions={"platform_family": "user@example.com"})
    with pytest.raises(ValueError, match="URL-like values"):
        MetricsBatch(counters={}, dimensions={"platform_family": "https://example.com"})


def test_metrics_require_minimum_group_size_for_reporting():
    with pytest.raises(ValueError, match="min_group_size"):
        MetricsBatch(counters={"app_opened": 1}, min_group_size=99)


def test_local_app_store_metrics_outputs_counts_only():
    state = {
        "contacts": {
            "alice": {"trust_state": "verified", "safety_short_code": "123-456", "peer_fingerprint": "secret"},
            "bob": {"trust_state": "unverified", "safety_short_code": "456-789", "peer_fingerprint": "secret"},
        },
        "messages": [
            {"contact": "alice", "direction": "sent", "body": "private message"},
            {"contact": "bob", "direction": "received", "body": "private reply"},
        ],
    }

    payload = local_app_store_metrics(state).to_dict()

    assert payload["counters"] == {
        "friends_added": 2,
        "verified_friends": 1,
        "unverified_friends": 1,
        "changed_friends": 0,
        "messages_sent": 1,
        "messages_received": 1,
    }
    serialized = repr(payload)
    assert "alice" not in serialized
    assert "bob" not in serialized
    assert "private message" not in serialized
    assert "123-456" not in serialized
    assert "fingerprint" not in serialized


def test_metrics_contract_lists_allowed_and_forbidden_fields():
    contract = metrics_contract()
    assert "messages_sent" in contract["allowed_counters"]
    assert "link_open_dismissed" in contract["allowed_counters"]
    assert "message_body" in contract["forbidden_keys"]
    assert "device_id" in contract["forbidden_keys"]
    assert "do not collect message content" in contract["rules"]
