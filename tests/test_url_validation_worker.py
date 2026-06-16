from __future__ import annotations

import pytest

from leftlevel_helix.url_validation_worker import (
    URL_VALIDATION_WORKER_CONTRACT_VERSION,
    UrlValidationResult,
    make_validation_request,
    worker_contract,
    worker_isolation_requirements,
)


def test_worker_request_has_contract_version_and_limits():
    request = make_validation_request("https://example.com", timeout_seconds=10)
    payload = request.to_dict()
    assert payload["v"] == URL_VALIDATION_WORKER_CONTRACT_VERSION
    assert payload["url"] == "https://example.com"
    assert payload["timeout_seconds"] == 10
    assert payload["max_redirects"] == 3
    assert payload["max_response_bytes"] == 1_000_000


def test_worker_request_rejects_bad_timeout():
    with pytest.raises(ValueError, match="timeout_seconds"):
        make_validation_request("https://example.com", timeout_seconds=0)
    with pytest.raises(ValueError, match="timeout_seconds"):
        make_validation_request("https://example.com", timeout_seconds=61)


def test_worker_result_does_not_allow_safe_claim():
    with pytest.raises(ValueError, match="unsupported URL validation verdict"):
        UrlValidationResult(request_id="abc", original_url="https://example.com", verdict="safe", reasons=[])


def test_worker_result_allows_no_obvious_risk_found():
    result = UrlValidationResult(
        request_id="abc",
        original_url="https://example.com",
        final_url="https://example.com/landing",
        verdict="no_obvious_risk_found",
        reasons=["worker found no obvious issue"],
        network_used=True,
    )
    payload = result.to_dict()
    assert payload["v"] == URL_VALIDATION_WORKER_CONTRACT_VERSION
    assert payload["verdict"] == "no_obvious_risk_found"
    assert payload["network_used"] is True


def test_worker_isolation_requirements_protect_app_state():
    requirements = worker_isolation_requirements()
    assert "no vault access" in requirements
    assert "no contacts access" in requirements
    assert "no message history access" in requirements
    assert "no user cookies" in requirements
    assert "no local-network access" in requirements
    assert "separate process or sandbox boundary" in requirements


def test_worker_contract_forbids_safe_language():
    contract = worker_contract()
    assert "safe" in contract["forbidden_verdicts"]
    assert "safe" not in contract["allowed_verdicts"]
    assert "no_obvious_risk_found" in contract["allowed_verdicts"]
    assert "never return safe" in contract["result_rule"]
