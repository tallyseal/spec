# CRAWCUS

**Contract · Receipt · Attestation · Warrant** — an open specification for cryptographic audit receipts that cover both application transactions and AI-inference decisions under one canonical shape.

---

## The problem CRAWCUS answers

When a regulator, auditor, or plaintiff asks *"prove this record has not been altered since it was written,"* the honest answer available today is usually one of:

- *"Trust our vendor's audit log"* — useless when the vendor is the defendant.
- *"Run our proprietary tool"* — a black box the regulator can't independently verify.
- *"Here are our SIEM logs"* — unsigned and mutable by anyone with SIEM admin.
- *"We put hashes on a blockchain"* — GDPR-incompatible at enterprise write throughput.

CRAWCUS makes a fourth answer possible: **replay the receipt chain against any conformant verifier and prove integrity mathematically, not by trusting a vendor.**

## What CRAWCUS is

Every CRAWCUS receipt is a small structured JSON document, signed with a key held by the customer, and appended to a hash-chained log where each entry references the hash of the previous one. Tampering with any historical record breaks the chain in a way any auditor can verify with an open-source tool in seconds.

The specification is deliberately not proprietary. Any party — systems integrator, adjacent vendor, individual developer, regulator — can implement a conformant runtime or verifier. A receipt standard that only one vendor can verify is not useful for compliance.

CRAWCUS composes existing open standards (JCS, SHA-256, RFC 3339, DSSE/Sigstore, VeritasChain erasable-immutable-log pattern). The value it adds is the *shape* — a specific set of fields, their meanings, and the two-scope coverage of both application and AI-inference decisions under one canonical form. The cryptographic primitives underneath are unchanged.

## Who this is for

| If you are a… | You care about |
|---|---|
| **Regulator or auditor** | Verifying a customer's receipt chain independently — without their cooperation, and without trusting the vendor that produced it. See the reference verifier in this repo. |
| **Compliance lead** (CISO, GRC, DPO, model-risk officer) | Answering procurement questionnaires and regulator letters with *"here is the open spec our system emits; you can verify without us"*. Anti-lock-in, anti-vendor-defendant-problem. |
| **Enterprise CTO or architect** | Evaluating whether a CRAWCUS-emitting product satisfies your walk-away, forensic-replay, and cross-runtime-audit requirements. |
| **Engineer building a conformant runtime** | Producing receipts that pass the Test Compatibility Kit (TCK) and consuming receipts from any other conformant runtime. Spec + TCK + reference verifier live here. |
| **Author of an adjacent open-source project** (federated learning, model serving, LLM observability, MLOps) | Adding a small reference client to your framework so your users get per-decision signed receipts. Existing examples: `clients/flower/`. |
| **Standards-body reviewer** | Assessing scope, governance trajectory, and prior-art composition ahead of a Linux Foundation / W3C / IETF conversation. |

## What's in this repository

| Path | What it is |
|---|---|
| `spec/` | The CRAWCUS specification — receipt shape, chain semantics, GDPR-erasure design, conformance rules. Licensed CC-BY-4.0. |
| `verifier/` | Reference verifier CLI — reads a CRAWCUS chain and reports chain integrity, signature validity, tombstone consistency, warrant resolution. Licensed Apache-2.0. |
| `tck/` | Test Compatibility Kit — portable JSON fixture set of receipts, chains, tombstones, and expected verification outcomes. Any runtime implementing CRAWCUS runs the TCK to prove conformance. Licensed Apache-2.0. |
| `clients/` | Reference client libraries for adjacent frameworks. Currently `clients/flower/` (per-node receipts for Flower federated-learning clients). Each client is a separate installable package. |
| `docs/` | How-to guides — verifying a chain, building a conformant runtime, delivering a chain to a regulator. |

## Quick start

**Verify a chain** (once verifier is published):

```bash
crawcus-verify chain.jsonl
# → chain integrity OK, 1,247 receipts, 0 tombstones, all warrants resolved
```

**Build a conformant runtime:** implement the receipt shape defined in `spec/README.md` §4, then run the TCK fixture set in `tck/`. Any language with JCS + SHA-256 + optional DSSE signing can produce conformant receipts.

**Add CRAWCUS to your framework:** see `clients/flower/` for a ~200-line reference client. The pattern generalises — hook wherever your framework surfaces a per-decision or per-call boundary.

## Status

CRAWCUS is at **specification version 1**. Reference implementations exist today for the receipt shape, hash-chain semantics, and one federated-learning client (Flower). Additional reference clients and language verifiers are on the roadmap; contributions welcome.

**Governance:** Foundry authors and maintains the specification today. Governance elevation to a neutral standards body (Linux Foundation / Joint Development Foundation) is in flight — the intent is a proper open-source-project governance model with multiple stewards, not a vendor-controlled specification. Progress is public in the repo's issue tracker.

**Openness:** we are careful with claims. Today CRAWCUS is *read-side open* — anyone can verify a chain independently of any vendor, and that is what buyers, regulators, and litigants actually rely on. The spec is published and can be implemented by anyone; conformant third-party implementations are welcomed. We do not claim "widely adopted" or "multi-vendor" ecosystem status we have not earned.

## Standards CRAWCUS builds on

CRAWCUS does not reinvent primitives. It composes:

- **JCS (RFC 8785)** for JSON canonical serialization
- **SHA-256** for chain linking
- **RFC 3339 / ISO 8601** for timestamps
- **DSSE + Sigstore** (optional) for signature envelope
- **VeritasChain Erasable Immutable Log** (2026) for tombstone / crypto-shred GDPR pattern
- **OAuth 2.0 / mTLS / SAML** actor-attribution conventions for the `actor` field

## Verify this release

All CRAWCUS-family packages published from this repository are signed via PyPI / npm Trusted Publishers with Sigstore attestations bound to the specific source commit + workflow run. Publishing an audit-integrity library without cryptographic supply-chain proof would be a self-contradiction.

Each release includes the exact `sigstore verify` command in its release notes.

## Contributing

CRAWCUS welcomes contributions from anyone building or evaluating cryptographic audit systems.

- **Spec-level discussions** — open an issue tagged `spec` on this repository. Changes to the receipt shape or chain semantics require spec-level discussion, not implementation-only PRs.
- **New reference clients** — for other federated-learning frameworks, model-serving platforms, LLM observability tools, or MLOps systems, open an issue tagged `client-proposal` first. See `docs/how-to-add-a-reference-client.md` for the fit test and package layout.
- **Additional language verifiers** — currently roadmapped: JavaScript / WASM, Python. Contributions to add Rust, Go, Java, or other languages welcome.
- **Conformance test fixtures** — the TCK is portable JSON; adding edge-case fixtures strengthens the whole ecosystem.

See `CONTRIBUTING.md` for the process. This project uses the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) v2.1.

## Licences

| Component | Licence |
|---|---|
| Specification text (`spec/`, this README, all `docs/`) | CC-BY-4.0 |
| Reference verifier, TCK, canonical hash implementations, reference clients (`verifier/`, `tck/`, `clients/`) | Apache-2.0 |

Third-party attributions in `NOTICE`.
