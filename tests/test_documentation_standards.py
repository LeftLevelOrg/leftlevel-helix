from __future__ import annotations

from pathlib import Path

DOCS = Path("docs")
FORBIDDEN_PUBLIC_PHRASES = [
    "for Danielle",
    "tonight",
    "my plan",
    "private conversation",
]


def test_public_docs_avoid_private_context_phrases():
    offenders: list[str] = []
    for path in DOCS.glob("*.md"):
        if path.name == "DOCUMENTATION_STANDARDS.md":
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_PUBLIC_PHRASES:
            if phrase.lower() in text.lower():
                offenders.append(f"{path}:{phrase}")
    assert offenders == []


def test_documentation_standards_exist():
    text = (DOCS / "DOCUMENTATION_STANDARDS.md").read_text(encoding="utf-8")
    assert "professional, neutral, project-focused" in text
    assert "Security language" in text


def test_project_values_are_documented():
    text = (DOCS / "PROJECT_VALUES.md").read_text(encoding="utf-8")
    assert "Security and privacy protection" in text
    assert "Fast and reliable messaging" in text
    assert "User-friendly interface" in text
    assert "Performance should not override the security model" in text


def test_website_messaging_brief_is_documented():
    text = (DOCS / "WEBSITE_MESSAGING_BRIEF.md").read_text(encoding="utf-8")
    assert "security-first open-source messaging protocol" in text
    assert "Secure by design" in text
    assert "Fast by engineering" in text
    assert "Usable by default" in text
    assert "not production-ready" in text


def test_repository_strategy_is_documented():
    text = (DOCS / "REPOSITORY_STRATEGY.md").read_text(encoding="utf-8")
    assert "leftlevel-helix" in text
    assert "leftlevel-app" in text
    assert "leftlevel-website" in text
    assert "leftlevel-relay" in text
    assert "Keep the playground in this repository for now" in text
    assert "Security-first rule" in text


def test_ui_extraction_plan_is_documented():
    text = (DOCS / "UI_EXTRACTION_PLAN.md").read_text(encoding="utf-8")
    assert "apps/desktop-playground" in text
    assert "LeftLevelOrg/leftlevel-app" in text
    assert "Extraction prerequisites" in text
    assert "UI milestones before extraction" in text
    assert "The app should call stable Helix interfaces" in text


def test_release_readiness_gates_are_documented():
    text = (DOCS / "RELEASE_READINESS_GATES.md").read_text(encoding="utf-8")
    assert "Current status" in text
    assert "protocol readiness" in text
    assert "user interface readiness" in text
    assert "Sign-off record template" in text
    assert "Blocking conditions" in text
