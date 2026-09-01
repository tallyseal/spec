# Decision lens — the three-lens test

> **Every product/strategy/scope/architecture/feature decision goes
> through three lenses. All three must be served, or the trade-off
> is surfaced out loud.**
>
> Adopted 2026-05-19. Canon — do not litigate. Update only by
> following the canon-edit discipline in `CLAUDE.md`.

## Why this exists

The notebook is large and the venture has a 10-year ambition. Without
a constant anchor, sessions drift:

- scope creep (e.g., decorative product surfaces)
- under-investment in moat-building (e.g., standards work, sector packs)
- tactical wins that don't compound (e.g., customer-specific shortcuts
  leaking into core packages)
- single-tenant / single-region / single-stack / single-buyer defaults
  that look fine at PR-1 but block the Year-7 outcome the moment scale
  arrives
- features that serve one buyer well but break another buyer's demo

The three-lens test prevents this. Every recommendation names which
markers, architectural defaults, and GTM motions it serves or
violates.

## Lens 1 — The 10-year North Star

Verbatim from `00-canon/identity.md`:

> Every AI interaction with a human in a regulated context — across
> health, education, legal, finance, government, and HR — runs on
> Tallyseal primitives, and the public record of that AI's decisions is
> auditable, replayable, and rights-respecting by default.

Supporting anchors:

- **Mission:** Make compliant AI the default. Replace *"AI is risky"*
  with *"AI is auditable."*
- **Category being defined:** AI Application Compliance Infrastructure
  (AACI). By 2027 a real Gartner category; Tallyseal is the top-right
  named player.
- **What customers pay for:** *covered* — they sleep at night because
  every AI action is recorded, explainable, defensible by construction.
  **Mechanism is the record; value is the relief.**
- **10-year end-state markers:** 5,000+ paid customers, 100,000+ OSS,
  $300-500M ARR, 8-10 sector overlays, IntentSpec adopted by ≥3
  frameworks beyond Tallyseal, IPO at $3-8B or strategic acquisition
  $1.5-4B.

## Lens 2 — The Year-7 Max plan

The upside / ceiling scenario Paul is steering toward (sourced from
`01-strategy/tam-sizing.md` and `05-narratives/investor-report.md`):

- **$300-500M ARR** by Year 7
- **Full Platform Edition** active — OEM embeds inside Salesforce /
  Anthropic / Microsoft (3-5 deals × ~$8M each)
- **Sector packs at full coverage** — 8-10 maintained (HIPAA, FERPA,
  GLBA, Legal-Privilege, EU AI Act High-Risk, ISO 42001, …)
- **Tallyseal Insurance MGA** operational, pricing premiums against
  telemetry
- **IntentSpec is de facto standard** for vertical AI agent compliance
  — ≥3 framework implementations beyond Tallyseal
- **Outcome:** IPO at $3-8B or strategic acquisition at $1.5-4B

### Architectural defaults the Year-7 Max plan forces — bake in from day 1

Every feature request, package decision, schema shape, or interface
design must assume these are true at build time, not retrofitted
later. **If a feature can't be shaped to scale across all of these,
surface the tension out loud.**

| Default | What it means for any feature decision |
|---|---|
| **Multi-tenant from day 1** | 5,000+ paid customers + hosted Cloud control plane. Every primitive (Intent, Event, Suggestion, Projection, Compliance Manifest) is tenant-scoped. No global state. Single-tenant code paths are technical debt the moment they ship. |
| **Multi-region from day 1** | EU residency is canon. Year 7 = EU + US + UK + APAC. No assumption of a single region for event store, PII vault, AI endpoint. Cross-region access throws by default. |
| **Multi-stack via ports** | OSS adapters for Prisma + Drizzle + Mongo + Supabase + Kysely + REST + GraphQL + tRPC + gRPC + Temporal. Never special-case Prisma; never let customer-specific stack assumptions leak into `@tallyseal/core`. |
| **Standards-grade IntentSpec** | W3C/IEEE submission within 12 months is LOCKED. Format must be implementation-independent — alternative implementations in Go/Rust/Python must be possible. Avoid coupling spec semantics to TS-language features. |
| **Federation + multi-org** | The fractal claim covers "Federated multi-org" and "Regulator-side ingestion." Year 7 = signed event exchange between organisations + regulator-side bundle ingestion. Event format portable and signable from day 1. |
| **OEM Platform Edition embeddability** | Year 3+ embeds Tallyseal inside Salesforce / Anthropic / Microsoft. Architecture must allow a platform partner — not the end customer — to own the Tallyseal runtime. |
| **Sector-pack composition is production-grade** | 8-10 overlays in production simultaneously. The `extends` mechanism on IntentSpec is load-bearing, conflict-resolving, versioned. Sector packs are first-class shippable artefacts. |
| **Regulator-facing endpoints** | Auditors + regulators consume signed event bundles directly. PII redaction, JSON-LD format, hash-chain verification, `npx witness audit-bundle` outputs are demo-grade from day 1. |
| **OSS-self-host completeness** | 100k+ OSS deployments. Runtime packages production-quality without the hosted Cloud admin UI. The admin UI is never a hard dependency for core flows. |
| **Eval-corpus shared moat** | Multi-tenant consent-gated eval-data sharing is architectural, not a feature add. |
| **Insurance-grade telemetry** | Tallyseal Insurance MGA prices premiums against telemetry. Privacy-preserving per-tenant telemetry export possible from day 1. |
| **Cross-border discipline** | `residency.crossBorderTransfers: 'forbid'` is the canon default. Multi-tenant means per-tenant residency, not one global setting. |

## Lens 3 — The multi-pronged GTM

Four motions running in parallel from day 1. Every feature decision
must work for **all four buyers simultaneously** — or the trade-off
is named explicitly.

| Motion | Buyer | What they touch | What this constrains in features |
|---|---|---|---|
| **Dev wedge** (OSS, bottom-up) | Senior engineers, eng leads, CTOs of dev-led shops | `@tallyseal/core`, CLI, adapters, GitHub repo, npm packages, docs | Every package MIT-licensed, npm-installable, work in <10 min quickstart. Standalone OSS path must reach production without ever talking to Cloud. The CLI (`migrate-form`, `generate`, `audit-bundle`) is *the* demo a dev shares on Twitter. |
| **Platform sale** (top-down, enterprise) | CISO, CIO, CFO, GC, board | Admin UI, audit viewer, sector packs, Cloud control plane, BYOC, SLA, signed audit bundles | Every feature must have a corresponding *demo surface* a CISO can be walked through in 15 minutes. Audit bundle + hash chain + compliance manifest UI are the demo. RBAC + compliance-officer veto are governance hooks they expect. |
| **Legal-led adoption** (counsel-driven) | General Counsel, Chief Privacy Officer, External Auditors | Audit viewer, DSAR endpoint, lawful-basis enforcement, Article-22 explanations, ediscovery export, sub-processor manifest | Legal buys *defensibility*. Every feature should make a litigation/regulator story easier, not harder. Plaintiff's case becomes *"Tallyseal wasn't enough"* not *"you have nothing."* When in doubt, the auditor's view is the design lens. |
| **Partner / Anthropic acquisition** | Platform-partner product leads, BD | `@tallyseal/ai-anthropic` adapter, Platform Edition embed APIs, co-marketing surface, neutral standards positioning | Tallyseal must be **acquirable by Anthropic specifically** — that's the named upside. Architecture keeps Anthropic as a first-class AI port (never lock-in OpenAI/Bedrock as default). Don't ship features that compete with Anthropic's core (model layer); ship features that compound Anthropic's product (application-layer compliance). Neutral standards positioning preserves multi-cloud partners. |

### How the four motions interlock

- The **dev wedge** earns the brand and seeds the bottom-up adoption flywheel.
- The **platform sale** converts CISO-budget into enterprise ARR (the Vanta/Drata ceiling).
- **Legal adoption** is the trojan horse — GCs forward the audit bundle to procurement, shortcuts sales cycles 50%.
- **Partner / Anthropic** is both upside and exit ($100-300M acquihire premium at $5M ARR Year 2-3 is a documented upside case).

If a feature serves only one motion, name which and what it costs the
others. If a feature serves three+, weight it heavily.

## How to apply

When evaluating a decision — large or small — answer in this shape:

1. **Lens 1 — North Star:** does this make it more likely that every
   regulated AI interaction runs on Tallyseal primitives in 10 years?
   Sideways or away → flag the trade-off.
2. **Lens 2 — Year-7 Max plan:** which architectural defaults does
   this honour? Which does it violate? Multi-tenant / multi-region /
   multi-stack / multi-locale / multi-version / federation-ready /
   OEM-embeddable / OSS-self-host-complete / regulator-facing.
3. **Lens 3 — Four-motion GTM:** which motions does this serve?
   Which does it cost? If only one motion served, name what's
   sacrificed for the others.

Then make the recommendation.

## What this rules out

- "Quick fix" feature shapes that bake in single-tenant or
  single-region assumptions
- Adapter coupling that privileges one stack (Prisma, Anthropic,
  Inngest) as a first-class default beyond what `integration-tiers.md`
  permits
- Features that compete with Anthropic's model-layer offering
- Surfaces (e.g., admin UI) introduced as hard dependencies of OSS
  core flows
- Customer-specific shortcuts inside packages destined for >1 customer
- Decisions made without naming which markers, defaults, and motions
  they serve

## References

- `00-canon/identity.md` — the North Star verbatim
- `01-strategy/tam-sizing.md` — Year-7 Max plan numbers
- `01-strategy/gtm-dual-entry.md` (stub — to be expanded with the four-motion model)
- `02-product/integration-tiers.md` — the multi-stack ports / adapters surface
- `02-product/compliance-manifest-schema.md` — multi-region residency + per-tenant defaults
- `05-narratives/investor-report.md` Sections 2 + 11 — the upside case and outcome shape
- `09-operating/decision-log.md` — LOCKED 2026-05-19 row that adopts this lens
