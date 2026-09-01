# SPDX-FileCopyrightText: 2026 Paul Wander + CRAWCUS contributors
# SPDX-License-Identifier: Apache-2.0
"""CrawcusClient — Flower NumPyClient mixin emitting per-`fit` CRAWCUS receipts."""
from __future__ import annotations

from typing import Any

try:
    from flwr.client import NumPyClient
except ImportError as e:
    raise ImportError(
        "crawcus-flower requires the Flower framework. Install with: pip install flwr"
    ) from e

from .chain import ReceiptStore
from .receipt import Receipt, now_iso


class CrawcusClient(NumPyClient):
    """Subclass and implement `_fit`, `actor`, `warrant`.

    Every `fit()` call emits a CRAWCUS receipt hash-chained to the previous one
    and appended to the ReceiptStore passed at construction.

    `evaluate()` receipts are banked — trigger: first user requests. See
    project_flower_ai_positioning_2026_09_01.md for the deferral rationale.
    """

    def __init__(self, store: ReceiptStore) -> None:
        super().__init__()
        self._store = store

    def actor(self) -> str:
        raise NotImplementedError("Subclass must implement actor() → identity string")

    def warrant(self, action: str) -> str:
        raise NotImplementedError("Subclass must implement warrant(action) → policy URI")

    def _fit(
        self, parameters: Any, config: dict[str, Any]
    ) -> tuple[Any, int, dict[str, Any]]:
        raise NotImplementedError("Subclass must implement _fit() with local training")

    def fit(
        self, parameters: Any, config: dict[str, Any]
    ) -> tuple[Any, int, dict[str, Any]]:
        new_params, num_examples, metrics = self._fit(parameters, config)
        receipt = Receipt(
            seq=self._store.next_seq(),
            action="flower.fit",
            args={"round": config.get("server_round"), "config": dict(config)},
            result={"num_examples": num_examples, "metrics": dict(metrics)},
            actor=self.actor(),
            warrant=self.warrant("flower.fit"),
            ts=now_iso(),
            prev_hash=self._store.prev_hash(),
        )
        self._store.append(receipt)
        return new_params, num_examples, metrics
