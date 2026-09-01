# SPDX-FileCopyrightText: 2026 Paul Wander + CRAWCUS contributors
# SPDX-License-Identifier: Apache-2.0
"""Per-node hash-chain state + JSONL persistence (spec §4 chain-link semantics)."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .receipt import Receipt


class ReceiptStore:
    """Append-only JSONL store. Recovers chain state on reopen."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self._seq = 0
        self._prev_hash: str | None = None
        if self.path.exists():
            for line in self.path.read_text().splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                self._seq = row["seq"]
                self._prev_hash = row["this_hash"]

    @classmethod
    def local_jsonl(cls, path: str | Path) -> "ReceiptStore":
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        return cls(p)

    def next_seq(self) -> int:
        return self._seq + 1

    def prev_hash(self) -> str | None:
        return self._prev_hash

    def append(self, receipt: Receipt) -> Receipt:
        sealed = receipt.sealed()
        with self.path.open("a") as f:
            f.write(json.dumps(asdict(sealed), separators=(",", ":")) + "\n")
        self._seq = sealed.seq
        self._prev_hash = sealed.this_hash
        return sealed
