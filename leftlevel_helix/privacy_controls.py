from __future__ import annotations

from dataclasses import asdict, dataclass

PRIVACY_CONTROLS_VERSION = "LLH-PRIVACY-CONTROLS-v0.1"


@dataclass(frozen=True)
class PrivacySettings:
    essential_service_metrics_enabled: bool = True
    optional_product_telemetry_enabled: bool = False
    local_diagnostics_enabled: bool = True
    user_can_disable_optional_telemetry: bool = True
    user_can_disable_essential_metrics: bool = False
    notice_required: bool = True

    def __post_init__(self) -> None:
        validate_privacy_settings(self)

    def to_dict(self) -> dict[str, object]:
        return {"v": PRIVACY_CONTROLS_VERSION, **asdict(self)}


def default_privacy_settings() -> PrivacySettings:
    return PrivacySettings()


def set_optional_product_telemetry(settings: PrivacySettings, enabled: bool) -> PrivacySettings:
    if not settings.user_can_disable_optional_telemetry:
        raise ValueError("optional telemetry must remain user-controllable")
    return PrivacySettings(
        essential_service_metrics_enabled=settings.essential_service_metrics_enabled,
        optional_product_telemetry_enabled=enabled,
        local_diagnostics_enabled=settings.local_diagnostics_enabled,
        user_can_disable_optional_telemetry=settings.user_can_disable_optional_telemetry,
        user_can_disable_essential_metrics=settings.user_can_disable_essential_metrics,
        notice_required=settings.notice_required,
    )


def telemetry_export_allowed(settings: PrivacySettings) -> bool:
    return settings.optional_product_telemetry_enabled and settings.user_can_disable_optional_telemetry


def validate_privacy_settings(settings: PrivacySettings) -> None:
    if not settings.essential_service_metrics_enabled:
        raise ValueError("essential service metrics must remain enabled for service operations")
    if settings.user_can_disable_essential_metrics:
        raise ValueError("essential service metrics are mandatory disclosed operations metrics")
    if not settings.user_can_disable_optional_telemetry:
        raise ValueError("optional product telemetry must be user-controllable")
    if not settings.notice_required:
        raise ValueError("privacy controls require clear user notice")


def privacy_controls_policy() -> dict[str, object]:
    return {
        "v": PRIVACY_CONTROLS_VERSION,
        "essential_service_metrics": "mandatory disclosed operations metrics",
        "optional_product_telemetry": "off by default and user-controllable",
        "local_diagnostics": "local-only and user-visible",
        "rules": [
            "essential service metrics cannot be disabled because they are required to operate the service",
            "essential service metrics require clear notice in privacy and terms language",
            "optional product telemetry defaults off",
            "optional product telemetry must be user-controllable",
            "remote optional telemetry export requires the optional telemetry setting to be enabled",
        ],
    }
