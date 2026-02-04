from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Optional

from restsync.auth import get_token
from restsync.canon import canonicalize
from restsync.http import request_json
from restsync.spec import EndpointSpec, RestsyncSpec, load_spec


class SnapshotError(RuntimeError):
    pass


def _format_url(spec: RestsyncSpec, template: str) -> str:
    return f"{spec.base_url}{template.format(owner=spec.repo.owner, repo=spec.repo.name)}"


def build_snapshot(
    spec: RestsyncSpec,
    token: Optional[str],
    *,
    request_func=request_json,
) -> Dict[str, Any]:
    endpoints = []
    for endpoint in sorted(spec.endpoints, key=lambda item: item.name):
        url = _format_url(spec, endpoint.url)
        live = request_func(
            endpoint.method,
            url,
            token,
            allow_not_found=endpoint.allow_not_found,
        )
        have = canonicalize(live, endpoint.compare)
        endpoints.append(
            {
                "name": endpoint.name,
                "url": url,
                "method": endpoint.method,
                "have": have,
            }
        )
    return {
        "version": spec.version,
        "provider": spec.provider,
        "base_url": spec.base_url,
        "repo": asdict(spec.repo),
        "endpoints": endpoints,
    }


def snapshot_from_path(path: Path) -> Dict[str, Any]:
    try:
        spec, errors = load_spec(path)
    except OSError as exc:
        raise SnapshotError(f"unable to read spec: {path}") from exc
    if errors or spec is None:
        raise SnapshotError("invalid spec: " + "; ".join(errors))
    token = get_token(spec.auth)
    return build_snapshot(spec, token)


def write_snapshot(snapshot: Dict[str, Any], output: Optional[Path]) -> None:
    payload = json.dumps(snapshot, indent=2, sort_keys=True)
    if output is None:
        print(payload)
        return
    output.write_text(payload + "\n", encoding="utf-8")
