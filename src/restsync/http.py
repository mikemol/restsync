from __future__ import annotations

import json
from typing import Any, Dict, Optional
from urllib.request import Request, urlopen


class HttpError(RuntimeError):
    pass


def request_json(
    method: str,
    url: str,
    token: Optional[str],
    body: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "restsync",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = Request(url, headers=headers, method=method, data=data)
    try:
        with urlopen(req) as resp:
            payload = resp.read().decode("utf-8")
    except OSError as exc:
        raise HttpError(f"request failed: {method} {url}") from exc
    if not payload:
        return {}
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise HttpError(f"invalid JSON response from {url}") from exc
