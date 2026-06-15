from __future__ import annotations

from pathlib import Path

REQUIRED_DOCS = {
    "README.md": ["Security status"],
    "CHANGELOG.md": ["Unreleased", "Known limitations"],
    "SECURITY_MODEL.md": ["Security"],
    "PRODUCTION_READINESS.md": ["Production"],
    "docs/PROJECT_VALUES.md": ["Security and privacy protection"],
    "docs/RELEASE_READINESS_GATES.md": ["Current status", "Sign-off record template", "Blocking conditions"],
    "docs/SIGNOFF_RECORD_TEMPLATE.md": ["Release candidate", "Gate status", "Evidence links", "Decision"],
    "docs/VERSIONING_POLICY.md": ["Package version", "Wire protocol name", "Changelog rule"],
    "docs/DEPENDENCY_INVENTORY.md": ["Runtime dependencies", "Production readiness requirements"],
    "docs/RELEASE_ARTIFACT_POLICY.md": ["Signing policy", "Reproducible build plan", "SBOM plan", "Rollback policy"],
    "docs/RELEASE_CHECKLIST.md": ["Prepare release candidate", "Build artifacts", "Sign-off"],
    "docs/CI_POLICY.md": ["Portable test suite", "Readiness documentation validation", "Production readiness boundary"],
    "docs/REPOSITORY_STRATEGY.md": ["Recommended repository boundaries"],
    "docs/UI_EXTRACTION_PLAN.md": ["Extraction prerequisites"],
    "docs/UI_PAIRING_FLOW.md": ["Pairing states", "Future pairing milestones", "Security boundary"],
    "docs/UI_SECURITY_LANGUAGE.md": ["User-facing names", "Color indicators", "Secure-by-default behavior"],
    "docs/UI_TESTING_RULES.md": ["Wording changes", "Color and text indicators", "Expected failures during iteration"],
    "docs/UI_FRIEND_VERIFICATION.md": ["Verify action", "Safety boundary", "Future improvements"],
    "docs/LOCAL_INTERFACE_TESTING.md": ["Current status"],
}


def validate_readiness_docs(root: Path = Path(".")) -> list[str]:
    failures: list[str] = []
    for relative_path, required_terms in REQUIRED_DOCS.items():
        path = root / relative_path
        if not path.exists():
            failures.append(f"missing required document: {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for term in required_terms:
            if term not in text:
                failures.append(f"{relative_path} missing required term: {term}")
    return failures


def main() -> int:
    failures = validate_readiness_docs()
    if failures:
        print("Release readiness validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Release readiness documentation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
