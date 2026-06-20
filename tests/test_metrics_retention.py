from __future__ import annotations

import pytest

from leftlevel_helix.metrics_retention import (
    METRICS_RETENTION_POLICY_VERSION,
    MetricsRetentionRule,
    default_retention_rules,
    metrics_retention_policy,
    validate_retained_payload,
)


def test_default_retention_rules_are_aggregate_only():
    rules = default_retention_rules()
    assert {rule.category for rule in rules} == {
        "essential_service_aggregate",
        "optional_product_aggregate",
        "security_abuse_aggregate",
        "local_only_user_visible",
    }
    for rule in rules:
        payload = rule.to_dict()
        assert payload["v"] == METRICS_RETENTION_POLICY_VERSION
        assert payload["aggregate_only"] is True
        assert payload["raw_event_logs_allowed"] is False
        assert payload["legal_review_required"] is True


def test_retention_rule_rejects_unknown_category():
    with pytest.raises(ValueError, match="unsupported metrics retention category"):
        MetricsRetentionRule("raw_event_logs", 1)


def test_retention_rule_rejects_overlong_retention():
    with pytest.raises(ValueError, match="exceeds category maximum"):
        MetricsRetentionRule("optional_product_aggregate", 366)


def test_retention_rule_rejects_raw_logs_and_non_aggregate_data():
    with pytest.raises(ValueError, match="aggregate-only"):
        MetricsRetentionRule("essential_service_aggregate", 30, aggregate_only=False)
    with pytest.raises(ValueError, match="raw event logs"):
        MetricsRetentionRule("essential_service_aggregate", 30, raw_event_logs_allowed=True)


def test_retention_rule_requires_legal_review():
    with pytest.raises(ValueError, match="legal review"):
        MetricsRetentionRule("essential_service_aggregate", 30, legal_review_required=False)


def test_validate_retained_payload_allows_aggregate_counts():
    validate_retained_payload({"messages_sent_total": 123, "delivery_failures_total": 2})


def test_validate_retained_payload_rejects_private_fields():
    for key in ["message_body", "contact_name", "url", "ip_address", "device_id", "filename", "safety_number"]:
        with pytest.raises(ValueError, match="forbidden retained metrics field"):
            validate_retained_payload({key: "secret"})


def test_metrics_retention_policy_documents_limits():
    policy = metrics_retention_policy()
    assert policy["v"] == METRICS_RETENTION_POLICY_VERSION
    assert policy["raw_event_log_retention_days"] == 0
    assert policy["retention_limits_days"]["essential_service_aggregate"] == 730
    assert policy["retention_limits_days"]["optional_product_aggregate"] == 365
    assert "message_body" in policy["forbidden_retention_fields"]
    assert "do not retain raw event logs for product analytics" in policy["rules"]
