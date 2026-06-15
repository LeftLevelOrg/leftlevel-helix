from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_VERSION = "LLH-ARTIFACT-MANIFEST-v0.1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(paths: list[Path], *, version: str | None = None) -> dict:
    artifacts = []
    for path in sorted(paths, key=lambda item: str(item)):
        if not path.is_file():
            raise ValueError(f"not a file: {path}")
        artifacts.append(
            {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return {
        "v": MANIFEST_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": version,
        "artifacts": artifacts,
    }


def write_manifest(manifest: dict, output: Path) -> None:
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a checksum manifest for release artifacts.")
    parser.add_argument("artifacts", nargs="+", help="Artifact files to include in the manifest.")
    parser.add_argument("--version", help="Release candidate or version label.")
    parser.add_argument("--out", default="artifact-manifest.json", help="Output manifest path.")
    args = parser.parse_args()

    manifest = build_manifest([Path(item) for item in args.artifacts], version=args.version)
    write_manifest(manifest, Path(args.out))
    print(f"wrote artifact manifest: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
