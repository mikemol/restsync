from __future__ import annotations

import os
import subprocess
from typing import Optional

from restsync.spec import AuthSpec


class AuthError(RuntimeError):
    pass


def _token_from_gh() -> str:
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise AuthError("failed to read token from gh auth") from exc
    token = result.stdout.strip()
    if not token:
        raise AuthError("gh auth token returned empty output")
    return token


def _token_from_env() -> str:
    token = os.environ.get("RESTSYNC_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise AuthError("missing RESTSYNC_TOKEN or GITHUB_TOKEN")
    return token.strip()


def get_token(auth: AuthSpec) -> Optional[str]:
    mode = auth.mode.strip().lower()
    if mode == "gh":
        return _token_from_gh()
    if mode in {"env", "token"}:
        return _token_from_env()
    if mode in {"none", ""}:
        return None
    raise AuthError(f"unsupported auth mode: {auth.mode}")
