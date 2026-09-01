# SPDX-FileCopyrightText: 2026 Paul Wander + CRAWCUS contributors
# SPDX-License-Identifier: Apache-2.0
"""Tests for CRAWCUS receipt shape + hash-chain semantics."""
from __future__ import annotations

import tempfile
from pathlib import Path

from crawcus_flower import Receipt, ReceiptStore


FIXED_TS = "2026-09-01T00:00:00Z"


def _receipt(seq: int, prev: str | None = None, actor: str = "node-1@test.example") -> Receipt:
    return Receipt(
        seq=seq,
        action="flower.fit",
        args={"round": 1, "config": {}},
        result={"num_examples": 100, "metrics": {"loss": 0.5}},
        actor=actor,
        warrant="test:warrant",
        ts=FIXED_TS,
        prev_hash=prev,
    )


def test_hash_is_deterministic() -> None:
    r = _receipt(1)
    assert r.compute_hash() == r.compute_hash()
    assert r.compute_hash().startswith("sha256:")


def test_hash_changes_on_field_change() -> None:
    r1 = _receipt(1)
    r2 = _receipt(1, actor="node-2@test.example")
    assert r1.compute_hash() != r2.compute_hash()


def test_hash_excludes_this_hash_field() -> None:
    r = _receipt(1)
    r.this_hash = "sha256:deadbeef"
    h1 = r.compute_hash()
    r.this_hash = "sha256:cafef00d"
    h2 = r.compute_hash()
    assert h1 == h2


def test_sealed_populates_this_hash() -> None:
    r = _receipt(1)
    sealed = r.sealed()
    assert sealed.this_hash == r.compute_hash()


def test_chain_persists_across_reopen() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "receipts.jsonl"

        store = ReceiptStore.local_jsonl(str(path))
        assert store.next_seq() == 1
        assert store.prev_hash() is None

        r1 = store.append(_receipt(1))
        r2 = store.append(_receipt(2, prev=r1.this_hash))
        assert r2.prev_hash == r1.this_hash

        reopened = ReceiptStore.local_jsonl(str(path))
        assert reopened.next_seq() == 3
        assert reopened.prev_hash() == r2.this_hash
