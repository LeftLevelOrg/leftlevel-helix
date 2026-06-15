from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

from .session import Envelope


class RelayClientError(RuntimeError):
    pass


@dataclass(frozen=True)
class HttpRelayClient:
    """Small stdlib HTTP client for the LeftLevel Helix prototype relay.

    The client intentionally sends only relay-visible envelope data: mailbox ID,
    authenticated header, and ciphertext. It does not send usernames, account IDs,
    plaintext, or conversation names.
    """

    base_url: str
    timeout: float = 10.0

    def __post_init__(self) -> None:
        if not self.base_url.startswith(("http://", "https://")):
            raise ValueError("relay base URL must start with http:// or https://")

    @property
    def normalized_base_url(self) -> str:
        return self.base_url.rstrip("/") + "/"

    def health(self) -> dict[str, Any]:
        return self._request_json("GET", "health")

    def put_envelope(self, envelope: Envelope) -> None:
        response = self._request_json("POST", "v0/envelopes", envelope.to_dict())
        if response.get("status") != "stored":
            raise RelayClientError(f"relay did not store envelope: {response!r}")

    def fetch_once(self, mailbox_id: str) -> Envelope | None:
        safe_mailbox = quote(mailbox_id, safe="")
        response = self._request_json("GET", f"v0/envelopes/{safe_mailbox}")
        if not response.get("found"):
            return None
        envelope = response.get("envelope")
        if not isinstance(envelope, dict):
            raise RelayClientError("relay returned malformed envelope response")
        return Envelope.from_dict(envelope)

    def _request_json(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        url = urljoin(self.normalized_base_url, path)
        data = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(url, data=data, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = response.read()
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RelayClientError(f"relay HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RelayClientError(f"relay connection failed: {exc.reason}") from exc
        except TimeoutError as exc:
            raise RelayClientError("relay request timed out") from exc

        try:
            decoded = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise RelayClientError("relay returned invalid JSON") from exc
        if not isinstance(decoded, dict):
            raise RelayClientError("relay returned non-object JSON")
        return decoded
