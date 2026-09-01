# SPDX-FileCopyrightText: 2026 Paul Wander + CRAWCUS contributors
# SPDX-License-Identifier: Apache-2.0
"""Minimal Flower client that emits CRAWCUS receipts per training round.

Run:
    pip install crawcus-flower
    python examples/quickstart.py
"""
from __future__ import annotations

from crawcus_flower import CrawcusClient, ReceiptStore


class HospitalNode(CrawcusClient):
    def actor(self) -> str:
        return "node-42@hospital-example.org"

    def warrant(self, action: str) -> str:
        return "gdpr-art-6-1-e:federated-ml-v1"

    def _fit(self, parameters, config):
        # Replace with real local training on your dataset.
        num_examples = 100
        metrics = {"loss": 0.42, "accuracy": 0.91}
        return parameters, num_examples, metrics


def main() -> None:
    store = ReceiptStore.local_jsonl("./receipts.jsonl")
    client = HospitalNode(store)

    # In real deployment:
    #   import flwr as fl
    #   fl.client.start_numpy_client(server_address="server:8080", client=client)
    #
    # For demo — call fit() directly to see a receipt land:
    _, n, metrics = client.fit(parameters=None, config={"server_round": 1})
    print(f"Round complete: {n} examples, metrics={metrics}")
    print(f"Receipt appended → {store.path}")


if __name__ == "__main__":
    main()
