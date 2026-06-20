from __future__ import annotations

import pytest

from leftlevel_helix.privacy_controls import (
    PRIVACY_CONTROLS_VERSION,
    PrivacySettings,
    default_privacy_settings,
    privacy_controls_policy,
    set_optional_product_telemetry,
    telemetry_export_allowed,
)


def test_default_privacy_settings_keep_optional_telemetry_off():
    settings = default_privacy_settings()
    payload = settings.to_dict()

    assert payload["v"] == PRIVACY_CONTROLS_VERSION
    assert settings.essential_service_metrics_enabled is True
    assert settings.optional_product_telemetry_enabled is False
    assert settings.local_diagnostics_enabled is True
    assert settings.user_can_disable_optional_telemetry is True
    assert settings.user_can_disable_essential_metrics is False
    assert settings.notice_required is True
    assert telemetry_export_allowed(settings) is False


def test_optional_product_telemetry_can_be_enabled_by_user_choice():
    settings = default_privacy_settings()
    enabled = set_optional_product_telemetry(settings, True)

    assert enabled.optional_product_telemetry_enabled is True
    assert telemetry_export_allowed(enabled) is True

    disabled = set_optional_product_telemetry(enabled, False)
    assert disabled.optional_product_telemetry_enabled is False
    assert telemetry_export_allowed(disabled) is False


def test_essential_service_metrics_cannot_be_disabled():
    with pytest.raises(ValueError, match="essential service metrics must remain enabled"):
        PrivacySettings(essential_service_metrics_enabled=False)


def test_essential_service_metrics_are_not_user_disableable():
    with pytest.raises(ValueError, match="mandatory disclosed operations metrics"):
        PrivacySettings(user_can_disable_essential_metrics=True)


def test_optional_telemetry_must_be_user_controllable():
    with pytest.raises(ValueError, match="optional product telemetry must be user-controllable"):
        PrivacySettings(user_can_disable_optional_telemetry=False)


def test_privacy_controls_require_notice():
    with pytest.raises(ValueError, match="clear user notice"):
        PrivacySettings(notice_required=False)


def test_privacy_controls_policy_documents_boundary():
    policy = privacy_controls_policy()

    assert policy["v"] == PRIVACY_CONTROLS_VERSION
    assert policy["essential_service_metrics"] == "mandatory disclosed operations metrics"
    assert policy["optional_product_telemetry"] == "off by default and user-controllable"
    assert "optional product telemetry defaults off" in policy["rules"]
    assert "remote optional telemetry export requires the optional telemetry setting to be enabled" in policy["rules"]
