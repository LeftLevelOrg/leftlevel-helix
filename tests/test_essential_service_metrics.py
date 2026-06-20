from __future__ import annotations

import pytest

from leftlevel_helix.essential_service_metrics import (
    ESSENTIAL_SERVICE_METRICS_VERSION,
    EssentialServiceMetricsReport,
    essential_service_metrics_policy,
)


def test_essential_service_metrics_report_exports_contract_version():
    report = EssentialServiceMetricsReport(
        counters={
            "registered_users_total": 500,
            "messages_sent_total": 1200,
            "delivery_failures_total": 4,
        },
        dimensions={"platform_family": "server", "release_channel": "prod"},
    )

    payload = report.to_dict()

    assert payload["v"] == ESSENTIAL_SERVICE_METRICS_VERSION
    assert payload["purpose"] == "service_operations"
    assert payload["notice_required"] is True
    assert payload["opt_in_required"] is False
    assert payload["upload_allowed"] is True
    assert payload["counters"]["messages_sent_total"] == 1200


def test_essential_service_metrics_are_mandatory_disclosed_not_opt_in():
    with pytest.raises(ValueError, match="mandatory disclosed operations metrics"):
        EssentialServiceMetricsReport(counters={"registered_users_total": 1}, opt_in_required=True)


def test_essential_service_metrics_require_clear_notice():
    with pytest.raises(ValueError, match="clear notice"):
        EssentialServiceMetricsReport(counters={"registered_users_total": 1}, notice_required=False)


def test_essential_service_metrics_reject_content_and_identifiers():
    for key in ["message_body", "contact_name", "url", "ip_address", "device_id", "filename", "safety_number"]:
        with pytest.raises(ValueError, match="forbidden essential metrics field"):
            EssentialServiceMetricsReport(counters={key: 1})


def test_essential_service_metrics_reject_unknown_counters():
    with pytest.raises(ValueError, match="unsupported essential metrics counter"):
        EssentialServiceMetricsReport(counters={"button_clicked": 1})


def test_essential_service_metrics_reject_identifier_dimensions():
    with pytest.raises(ValueError, match="must not contain identifiers"):
        EssentialServiceMetricsReport(
            counters={"registered_users_total": 1},
            dimensions={"platform_family": "device-abc"},
        )
    with pytest.raises(ValueError, match="unsupported essential metrics dimension"):
        EssentialServiceMetricsReport(
            counters={"registered_users_total": 1},
            dimensions={"device_id": "abc"},
        )


def test_essential_service_metrics_policy_documents_boundary():
    policy = essential_service_metrics_policy()
    assert policy["status"] == "mandatory_disclosed_operations_metrics"
    assert policy["opt_in_required"] is False
    assert policy["notice_required"] is True
    assert "messages_sent_total" in policy["allowed_counters"]
    assert "registered_users_total" in policy["allowed_counters"]
    assert "message_body" in policy["forbidden_fields"]
    assert "device_id" in policy["forbidden_fields"]
    assert "collect only aggregate counters needed to operate and support the service" in policy["rules"]
    assert "do not use essential metrics for advertising, cross-app tracking, or data broker sharing" in policy["rules"]
