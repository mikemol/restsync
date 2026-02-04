from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass(frozen=True)
class RepoSpec:
    owner: str
    name: str


@dataclass(frozen=True)
class AuthSpec:
    mode: str


@dataclass(frozen=True)
class CompareSpec:
    include: List[str] = field(default_factory=list)
    ignore: List[str] = field(default_factory=list)
    sort: List[str] = field(default_factory=list)
    unwrap_enabled: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ApplySpec:
    method: str
    url: str
    body_from: str


@dataclass(frozen=True)
class EndpointSpec:
    name: str
    method: str
    url: str
    compare: CompareSpec
    allow_not_found: bool = False
    apply: Optional[ApplySpec] = None


@dataclass(frozen=True)
class RestsyncSpec:
    version: int
    provider: str
    repo: RepoSpec
    base_url: str
    auth: AuthSpec
    desired: Dict[str, Any]
    endpoints: List[EndpointSpec]
    overlay: Optional[str] = None


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _require_str(value: Any, label: str, errors: List[str]) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    errors.append(f"{label} must be a non-empty string")
    return ""


def _load_compare(raw: Dict[str, Any]) -> CompareSpec:
    include = [str(item) for item in raw.get("include", [])]
    ignore = [str(item) for item in raw.get("ignore", [])]
    sort = [str(item) for item in raw.get("sort", [])]
    unwrap_enabled = [str(item) for item in raw.get("unwrap_enabled", [])]
    return CompareSpec(
        include=include,
        ignore=ignore,
        sort=sort,
        unwrap_enabled=unwrap_enabled,
    )


def _load_apply(raw: Dict[str, Any], errors: List[str], label: str) -> Optional[ApplySpec]:
    if not isinstance(raw, dict):
        errors.append(f"{label} must be a mapping")
        return None
    method = _require_str(raw.get("method"), f"{label}.method", errors).upper()
    url = _require_str(raw.get("url"), f"{label}.url", errors)
    body_from = _require_str(raw.get("body_from"), f"{label}.body_from", errors)
    if method and method not in {"PUT", "PATCH", "POST"}:
        errors.append(f"{label}.method must be PUT, PATCH, or POST")
    if url and not url.startswith("/"):
        errors.append(f"{label}.url must start with '/' (got {url!r})")
    return ApplySpec(method=method, url=url, body_from=body_from)


def load_spec(path: Path) -> tuple[Optional[RestsyncSpec], List[str]]:
    data = _load_yaml(path)
    errors: List[str] = []

    version_raw = data.get("version")
    if isinstance(version_raw, int):
        version = version_raw
    else:
        errors.append("version must be an integer")
        version = 0
    provider = _require_str(data.get("provider"), "provider", errors)
    base_url = _require_str(data.get("base_url"), "base_url", errors)
    overlay = data.get("overlay")
    if overlay is not None and not isinstance(overlay, str):
        errors.append("overlay must be a string path if provided")
        overlay = None

    repo_raw = data.get("repo", {})
    if not isinstance(repo_raw, dict):
        errors.append("repo must be a mapping")
        repo_raw = {}
    repo = RepoSpec(
        owner=_require_str(repo_raw.get("owner"), "repo.owner", errors),
        name=_require_str(repo_raw.get("name"), "repo.name", errors),
    )

    auth_raw = data.get("auth", {})
    if not isinstance(auth_raw, dict):
        errors.append("auth must be a mapping")
        auth_raw = {}
    auth = AuthSpec(mode=_require_str(auth_raw.get("mode"), "auth.mode", errors))

    desired = data.get("desired", {})
    if not isinstance(desired, dict):
        errors.append("desired must be a mapping")
        desired = {}

    endpoints_raw = data.get("endpoints", [])
    if not isinstance(endpoints_raw, list):
        errors.append("endpoints must be a list")
        endpoints_raw = []

    endpoints: List[EndpointSpec] = []
    seen_names: set[str] = set()
    for idx, raw in enumerate(endpoints_raw):
        label = f"endpoints[{idx}]"
        if not isinstance(raw, dict):
            errors.append(f"{label} must be a mapping")
            continue
        name = _require_str(raw.get("name"), f"{label}.name", errors)
        method = _require_str(raw.get("method"), f"{label}.method", errors).upper()
        url = _require_str(raw.get("url"), f"{label}.url", errors)
        if name in seen_names:
            errors.append(f"{label}.name must be unique (duplicate {name!r})")
        if url and not url.startswith("/"):
            errors.append(f"{label}.url must start with '/' (got {url!r})")
        if method and method not in {"GET", "POST", "PUT", "PATCH"}:
            errors.append(f"{label}.method must be GET, POST, PUT, or PATCH")
        compare_raw = raw.get("compare", {})
        if compare_raw is None:
            compare_raw = {}
        if not isinstance(compare_raw, dict):
            errors.append(f"{label}.compare must be a mapping")
            compare_raw = {}
        compare = _load_compare(compare_raw)
        allow_not_found = raw.get("allow_not_found", False)
        if allow_not_found not in (True, False):
            errors.append(f"{label}.allow_not_found must be a boolean")
            allow_not_found = False
        apply_spec = None
        if "apply" in raw:
            apply_spec = _load_apply(raw.get("apply"), errors, f"{label}.apply")
        endpoints.append(
            EndpointSpec(
                name=name,
                method=method,
                url=url,
                compare=compare,
                allow_not_found=allow_not_found,
                apply=apply_spec,
            )
        )
        if name:
            seen_names.add(name)

    if errors:
        return None, errors

    return (
        RestsyncSpec(
            version=version,
            provider=provider,
            repo=repo,
            base_url=base_url,
            auth=auth,
            desired=desired,
            endpoints=endpoints,
            overlay=overlay,
        ),
        [],
    )


def validate_spec(path: Path) -> List[str]:
    _, errors = load_spec(path)
    return errors
