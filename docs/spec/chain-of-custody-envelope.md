<!--
SPDX-FileCopyrightText: 2026 Paul Wander + CRAWCUS contributors
SPDX-License-Identifier: CC-BY-4.0
-->

# The chain-of-custody envelope around the decisioning core

*A one-page brief — June 2026.*

---

The regulatory wave hitting automated decisions about people asks one
question, in one shape: *"Show me why this decision about this individual was
lawful at the moment it was made — on what basis, with what oversight, by
which model and version, with which consent state, and with the input lineage
that produced it."* EU AI Act Annex III high-risk regime enters enforcement
2 August 2026. GDPR Article 22 explanations run on a 30-day clock. FRE 901
and EU evidence rules are being applied to AI outputs for the first time.
The question is engine-agnostic. **The answer that satisfies a regulator has
to hold across every decision the customer makes about the individual — not
only the ones that flowed through one engine.**

FICO has been answering that question at the FICO-engine layer for 25 years
with a depth no other vendor matches. *"Every decision is logged, traced, and
explained"* is not marketing copy when FICO writes it — it is the load-bearing
discipline of FICO Platform, descending from Scott Zoldi's 1998 explainability
patents and refined through Blaze Advisor, Strategy Director, Falcon, and
Analytics Workbench. The FFM line extends it for the generative wave. If the
customer's decision flows through FICO, the auditor has a clean answer.

## The scope clause that the next wave forces into view

The scope, named on FICO's own Operational Data Transparency page, is
*"every execution flowing through FICO Platform."* That clause is correct,
honest, and load-bearing — and the operating reality on the customer side
is that not every regulated automated decision about the same individual
flows through FICO Platform.

A consumer-lending customer scores credit through FICO **and** runs a
generative onboarding assistant, an LLM-backed dispute triage, a rules
engine for fee waivers, an HR-eligibility model for collections agent
assignment, and a human sign-off on adverse-action review. Each of those is
a regulated automated decision under Article 22, Article 14, GDPR Article 35,
FCRA, ECOA Reg B, or all of them. None of them flows through FICO Platform.
The auditor's question does not distinguish: they want the chain of custody
on the individual, across every decision the institution made.

This is the gap. Not a FICO defect — a scope clause being met by the world
moving past it. FICO Platform is the depth player for FICO-engine decisions;
the customer needs an envelope above every engine they run.

## What Tallyseal is

Tallyseal is the horizontal, engine-agnostic chain-of-custody runtime that
sits underneath every automated decision the application makes — LLM call,
classical ML scorecard, deterministic rules engine, or human sign-off
layered on any of them — and emits a hash-chained, regulation-typed receipt
at the moment of determination.

The mechanism is a fourteen-primitive surface, eight of them load-bearing
for the chain: **Contract · Receipt · Attestation · Warrant · Consent ·
Lineage · Disclosure · HumanOversight**. Each is a typed callable, not a
YAML policy reference: `gdpr.art8.minorConsent(opts)`, `euAct.art14(opts)`,
`hipaaSafeHarbor(opts)`, `ferpa.s9931(opts)`. The receipt carries lawful
basis, consent state, oversight outcome, model and prompt version, input
lineage, and the output itself, hash-chained for tamper-evidence and
verifiable offline by any third party.

The runtime ships MIT under `@tallyseal/*` on npm; the spec is **CRAWCUS**
(Contract · Receipt · Attestation · Warrant — Compliance Unified
Specification), targeting W3C / IEEE / ISO submission. The receipt
wire-format is byte-compatible with the IETF Acta draft
(`draft-farley-acta-signed-receipts-01`) — same Ed25519, same JCS-canonical
hash-chain envelope — with the regulation-binding semantics that the
substrate layer does not address layered above. Microsoft Agent Governance
Toolkit, AWS Cedar, Sigstore Rekor, Pydantic AI, LlamaIndex, LangChain,
and Vercel AI are aligned at the substrate. Tallyseal is the regulation
layer on top of that substrate.

## Where this composes with FICO Platform

The customer who runs FICO Platform for FICO-engine decisions and Tallyseal
for the cross-engine envelope gets two artefacts the auditor verifies
independently:

- FICO's native decision audit, explainability, and lineage for every
  decision through FICO's engines — unchanged, the system of record at
  the FICO layer.
- A Tallyseal CRAWCUS receipt for every decision the application made,
  whatever the engine, including the FICO ones (as cross-engine envelopes
  pointing into FICO Platform's deeper record), verifiable offline by the
  auditor's own copy of the CRAWCUS verifier.

The chain of custody holds across the whole stack. FICO Platform's
twenty-five years of evidentiary discipline at the FICO layer reaches the
LLM-driven and bespoke decisions the same customer also has to defend.
Neither layer competes with the other; the customer gets both, and the
regulator gets the engine-agnostic envelope that the audit obligation
actually requires.

## Three shapes this could take

Naming the shapes; not asking. The pre-incorporation founder is the
decision-maker on the Tallyseal side.

- **Adapter** — `@tallyseal/fico-platform` ships open-source against
  FICO Platform's existing logging surfaces; FICO Platform decisions get
  the cross-engine envelope for free; no commercial relationship required.
- **OEM** — FICO Platform ships Tallyseal under the FICO brand as the
  cross-engine layer; FICO carries CRAWCUS to its enterprise channel;
  joint authorship of the W3C / IEEE submission strengthens FICO's
  standards posture and Tallyseal's vendor-neutrality.
- **Acquisition** — Tallyseal folds into FICO; CRAWCUS proceeds under
  joint authorship; the cross-engine layer becomes part of FICO Platform
  the way explainability did in 1998.

## What this brief is and is not

- Not a claim that FICO Platform doesn't do explainability or audit. It
  does, with a depth nothing else in the market touches. The claim is
  that the scope clause names a clear boundary the regulatory wave is
  asking the customer to step over.
- Not a substitute for FICO's relationship with the regulator or the
  Big-4. CRAWCUS aims at W3C / IEEE / ISO precisely because vendor-neutral
  standards-body adoption is how the receipt format earns admissibility
  across jurisdictions.
- Not a SaaS competitor. The runtime is MIT-licensed and self-hostable;
  commercial revenue sits above the OSS in operated services
  (notary-signed bundles, sector-pack attestations, federation, MGA
  conformity workflows).
- Not a soft ask for a meeting. If the gap above resonates with what
  you see in your customer base, the founder welcomes a conversation.
  Paid engagement; NDA before architecture or customer specifics.

## About this brief

Distribution: pre-NDA shareable. Tallyseal, Inc. (incorporation pending).
Paul Wander, founder — paul@thewanders.com. This document contains no
confidential information.

<!-- glossary-appendix:start -->

---

## Glossary

| Term | Definition |
| --- | --- |
| **CRAWCUS** | Contract · Receipt · Attestation · Warrant — Compliance Unified Specification. The open standard authored by Tallyseal; vendor-neutral, MIT-licensed. Lives at @crawcus/* npm packages; reference runtime is @tallyseal/*. |
| **EU AI Act** | Regulation (EU) 2024/1689 — entered force August 2024. Risk-tiered (prohibited / high-risk / limited / minimal); high-risk uses listed in Annex III; Article 14 mandates human oversight. |
| **GDPR** | General Data Protection Regulation (EU 2016/679) — entered force May 2018. Article 22 governs solely-automated decisions; Article 35 mandates DPIAs for high-risk processing. |
| **IEEE** | Institute of Electrical and Electronics Engineers — standards body Tallyseal targets for the CRAWCUS open-spec spin-out. |
| **ISO** | International Organization for Standardization — publisher of ISO/IEC 27001 (information security) and ISO/IEC 42001 (AI management systems). |
| **LLM** | Large Language Model — generative AI model (GPT-class, Claude-class) trained on broad text corpora. |
| **MGA** | Managing General Agent — an insurance intermediary with delegated underwriting authority on behalf of a carrier. |
| **MIT** | MIT License — a permissive open-source licence; both @crawcus/* (spec) and @tallyseal/* (reference runtime) ship MIT. |
| **ML** | Machine Learning — broader category that includes LLMs, classical scorecards, and other model classes. |
| **NDA** | Non-Disclosure Agreement. |
| **OEM** | Original Equipment Manufacturer — used here for white-label / re-badged distribution arrangements. |
| **OSS** | Open Source Software. |
| **W3C** | World Wide Web Consortium — standards body Tallyseal targets for the CRAWCUS open-spec spin-out alongside IEEE. |
| **Warrant** | One of CRAWCUS's 14 primitives — the explicit, machine-readable legal-basis declaration paired with each Contract (e.g. GDPR Article 6(1)(b), FERPA §99.31(a)(1)). |

*Generated from `docs/notebook/09-operating/glossary.csv` — edit there, then run `node tools/render-glossary.mjs <file>` to refresh.*

<!-- glossary-appendix:end -->
