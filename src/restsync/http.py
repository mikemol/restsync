from __future__ import annotations

import json
from typing import Any, Dict, Optional
from urllib.request import Request, urlopen


class HttpError(RuntimeError):
    pass


def request_json(method: str, url: str, token: Optional[str]) -> Dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "restsync",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers, method=method)
    try:
        with urlopen(req) as resp:
            payload = resp.read().decode("utf-8")
    except OSError as exc:
        raise HttpError(f"request failed: {method} {url}") from exc
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise HttpError(f"invalid JSON response from {url}") from exc
