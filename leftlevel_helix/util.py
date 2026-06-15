from __future__ import annotations

import base64
import json
from typing import Any


def b64e(data: bytes) -> str:
    """URL-safe base64 without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64d(text: str) -> bytes:
    """Decode URL-safe base64 without padding."""
    padding = "=" * ((4 - len(text) % 4) % 4)
    return base64.urlsafe_b64decode((text + padding).encode("ascii"))


def canonical_json(obj: Any) -> bytes:
    """Canonical JSON for transcript/AAD binding."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
