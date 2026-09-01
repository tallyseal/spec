# SPDX-FileCopyrightText: 2026 Paul Wander + CRAWCUS contributors
# SPDX-License-Identifier: Apache-2.0
"""CRAWCUS receipt shape + JCS+SHA-256 hashing (spec §4, §7)."""
from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

import jcs


@dataclass
class Receipt:
    seq: int
    action: str
    args: dict[str, Any]
    result: dict[str, Any]
    actor: str
    warrant: str
    ts: str
    prev_hash: str | None = None
    warrant_body: str | None = None
    this_hash: str = ""

    def compute_hash(self) -> str:
        body = {k: v for k, v in asdict(self).items() if k != "this_hash" and v is not None}
        canonical = jcs.canonicalize(body)
        return "sha256:" + hashlib.sha256(canonical).hexdigest()

    def sealed(self) -> "Receipt":
        return Receipt(**{**asdict(self), "this_hash": self.compute_hash()})


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
