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
