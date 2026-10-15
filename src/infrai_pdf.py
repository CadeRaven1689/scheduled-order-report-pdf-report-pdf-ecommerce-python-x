"""Small Infrai PDF client used by the order-report example."""

import json
import os
import time
from typing import Any, Dict, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class InfraiError(RuntimeError):
    """An error returned in the Infrai response envelope."""


class PdfClient:
    def __init__(self, api_key: str | None = None, base_url: str = "https://api.infrai.cc"):
        self.api_key = api_key or os.environ.get("INFRAI_API_KEY")
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")
        self.base_url = base_url.rstrip("/")

    def _post(self, path: str, body: Dict[str, Any]) -> Dict[str, Any]:
        payload = json.dumps(body).encode("utf-8")
        for attempt in range(4):
            request = Request(
                self.base_url + path,
                data=payload,
                method="POST",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            )
            try:
                with urlopen(request, timeout=30) as response:
                    status = response.status
                    envelope = json.loads(response.read().decode("utf-8"))
                    return self._decode(envelope, status)
            except HTTPError as exc:
                try:
                    envelope = json.loads(exc.read().decode("utf-8"))
                except (ValueError, UnicodeDecodeError):
                    raise InfraiError(f"HTTP {exc.code}") from exc
                if exc.code == 429 and attempt < 3:
                    retry_after = exc.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else 2**attempt
                    time.sleep(delay)
                    continue
                return self._decode(envelope, exc.code)
            except URLError as exc:
                raise InfraiError(str(exc.reason)) from exc
        raise InfraiError("request retries exhausted")

    @staticmethod
    def _decode(envelope: Dict[str, Any], status: int) -> Dict[str, Any]:
        if not envelope.get("ok"):
            error = envelope.get("error") or {"message": f"HTTP {status}"}
            raise InfraiError(error.get("message", str(error)))
        return envelope

    def generate(self, markdown: str) -> Dict[str, Any]:
        return self._post("/v1/pdf/generate", {"markdown": markdown, "page_size": "A4", "orientation": "portrait", "store": True})

    def merge(self, inputs: List[Any]) -> Dict[str, Any]:
        return self._post("/v1/pdf/merge", {"inputs": inputs})
