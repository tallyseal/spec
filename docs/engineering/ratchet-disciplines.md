# Engineering ratchet disciplines

> A ratchet has one direction. Once installed, the bar only rises.
> For a compliance product, regression = lost customers + regulatory exposure.

Disciplines 1–12 are *invariants of correctness* (the original ratchet).
Disciplines 13–17 are *invariants of session hygiene* — inherited from
sister projects (`HF`, `ep`, `gps-action`) where they're load-bearing for
multi-session, parallel-agent work.
Disciplines 18–19 added 2026-05-20 — capability-based security +
total-function discipline.
Disciplines 20–22 added 2026-05-21 — discipline-wiring sprint;
explicit throw discipline, fast-lane commit hygiene, post-commit
async test safety net.
Discipline 23 added 2026-05-21 — CRAWCUS-vs-Tallyseal boundary;
preserves vendor-neutrality of the open spec ahead of Y1 H2
structured spin-out (per decision-log B1.3b).

## Wired-status legend

| Symbol | Meaning |
|---|---|
| ✅ | Wired + enforced (CI / pre-commit / lint rule fires on violation) |
| ⚠️ | Documented + partially enforced (gap surfaces somewhere but not everywhere) |
| 📋 | Documented; manual discipline (no automation possible / available yet) |
| ⏳ | Pending wiring (next sprint) |

## The 23 disciplines

| # | Discipline | Wired | Practice | Why it ratchets |
|---|---|---|---|---|
| 1 | **TypeScript strict, zero `any`, zero `@ts-ignore`** | ✅ | `tsconfig.base.json` strict+exactOptionalPropertyTypes+noUncheckedIndexedAccess. Pre-commit `pnpm typecheck`. Lint `@typescript-eslint/no-explicit-any`. CI gate. | Type erosion is #1 maintenance debt; start at zero, count is the metric |
| 2 | **Property-based + mutation testing on compliance code** | ⚠️→✅ | Property-based: fast-check used in core (canonical-json + hash-chain). Mutation: Stryker config at `stryker.conf.json`; `pnpm test:mutation`; `.github/workflows/mutation.yml` runs on PR + nightly. **Two thresholds**: (a) `thresholds.break: 70` on the **inclusive** score (Stryker-enforced workspace gate); (b) **discipline target ≥80% covered AGGREGATE per workspace mutate-set** (not per-file). Per-file scores below 80% covered are acceptable when the aggregate clears 80% — clarified 2026-06-04 in lighthouse review of PR #63 / TKT-ADMIN-EMITTER-ROUNDTRIP (aggregate 80.10% covered, `parse.ts` 77.66%, `roundtrip.ts` 60%) so Sprint E precedent doesn't quietly lower the bar. Per-ticket TKT-spec "Stryker ≥80% covered on `src/{a,b,c}.ts`" wording reads as aggregate across that mutate-set unless explicitly stated per-file. | Compliance code has too many edge cases for example-based tests |
| 3 | **Deterministic reducer (pure, hash-tested)** | ⚠️ | `assertReducerDeterminism` in `@tallyseal/core`; tested. CI gate via Stryker on `reducer/`. | Single load-bearing correctness property. Auditors will recompute. |
| 4 | **Forward-only migrations + two-release deprecation window** | ⚠️ | `@tallyseal/prisma-adapter` migration runner enforces SHA-256 checksum immutability (refuses re-apply of edited files). No broader workspace-wide auto-check yet. | Eliminates data-loss + downtime. Customers can replay history forever. |
| 5 | **Conventional + signed commits, signed tags, SBOM on every build** | ⚠️→✅ | Conventional: commitlint pre-commit hook ✅. Signed: documented; user-side `git config commit.gpgsign true` (out of repo's control). SBOM: `.github/workflows/security.yml` generates CycloneDX SBOM on every push + archives as artifact. | Supply chain attacks are the realistic threat; SBOM diff = auditor-recognised chain of custody |
| 6 | **Trunk-based, feature-flagged, no long-lived branches** | ✅ | Trunk-based; feature flags not yet needed. | Long branches → merge hell + stealth regressions |
| 7 | **Eval corpus regression — production transcripts as fixtures** | ⚠️ | `@tallyseal/extractor` ships `runEvalCorpus` + `checkRegression`; CI runs on PRs touching extractor. Per-spec pass-rate gate at 0.5pp tolerance. (No production corpus yet — Q7 LOCKED: synthetic-only v0.0.1.) | The eval corpus IS the moat. Regression metric → it compounds. |
| 8 | **Blameless postmortem in 72h with structural action item** | 📋 | No incidents yet. Discipline + template land when the first incident does. | Without structural action, postmortems become theatre |
| 9 | **Threat model + PIA per IntentSpec change** | ⚠️ | `.github/pull_request_template.md` includes a STRIDE + LINDDUN + DPIA prompt. PR reviewer enforcement (no automation possible for content quality). | EU AI Act + GDPR Art. 35 require this for high-risk systems |
| 10 | **Compliance regression tests — one per regulation article** | ⚠️ | Tests exist for GDPR Art. 8, FERPA §99.31, EU AI Act Art. 14. **Compliance Coverage Matrix doc pending** — until landed, no automated "claim → test" assertion. | Marketing claims become falsifiable. Auditors can run them. |
| 11 | **Performance budget + observability budget per endpoint** | ✅ | `.size-limit.cjs` per-package gzip budgets; `pnpm test:size` enforced in CI. `pnpm test:bench` (vitest bench) + bench-output artifact archived per CI run. | Compliance products live or die on uptime + latency |
| 12 | **Break-glass production access only, logged + reviewed weekly** | 📋 | No production yet. | Trust story collapses if employees can quietly read customer data |
| 13 | **Sealed mutation path — only `writeEvent` mutates** | ✅ | Custom ESLint rule `tallyseal/no-direct-prisma-create` in `@tallyseal/eslint-config` blocks `<client>.<model>.{create,update,upsert,delete,createMany,updateMany,deleteMany}()` outside writeEvent + prisma-adapter. Exempt token `// sealed-mutation-exempt: <reason>` counted by CI. | Architectural invariant: one mutation path; cannot be circumvented under deadline pressure |
| 14 | **Conventional commits + commitlint + husky** | ✅ | husky `commit-msg` hook + commitlint with `@commitlint/config-conventional`. 100-char header. CI gate via commitlint. | Tooling derives changelogs, version bumps, audit-trail granularity from commit history |
| 15 | **Branch naming with date suffix** | 📋 | Solo on main; not enforced. Re-evaluates when parallel sessions or first hire lands. | Prevents parallel Claude Code sessions colliding on the same branch name — a silent-corruption risk under multi-agent work |
| 16 | **Version bump per PR (PATCH minimum)** | ✅ | `.github/workflows/version-check.yml` blocks merge if `packages/*/src/**` or `packages/*/migrations/**` changed without bumping the package's `version`. | Every change is small, traceable, reversible; `git bisect` works; tag-per-PR auto-generates release notes |
| 17 | **Worktree per session for parallel work** | 📋 | Solo; not enforced. Re-evaluates when parallel sessions land. | Eliminates branch-clash between parallel sessions — `git checkout` in one session silently moves HEAD in the other |
| 18 | **No ambient authority** (capability-based security discipline) | ✅ | Custom ESLint rule `tallyseal/no-ambient-authority` flags module-scope `process.env.X`, module-scope `new <Client\|Pool\|Adapter\|Service\|Manager>(...)`, any `globalThis.X`. Exempt token `// capability-exempt: <reason>` counted by CI. | Multi-tenant safety becomes structural, not reviewer-dependent. Cross-tenant leaks become impossible-by-construction rather than caught-in-PR. Capability audit logs become litigation gold (Lens 3 legal motion). OEM Platform Edition embeddability requires zero singletons / zero process-globals; this rule pre-empts the retrofit cost. |
| 19 | **Total functions + exhaustive matching** | ✅ | Custom ESLint rule `tallyseal/throw-only-typed-errors` — throws MUST be `throw new <SomeError>(...)` constructions, never bare values / strings / objects. Backstopped by tsconfig `noFallthroughCasesInSwitch` + `assertNever` discipline in default branches. (`@typescript-eslint/switch-exhaustiveness-check` available behind type-aware-lint opt-in.) | Replayability holds under all inputs. Errors are values (`Result<T, E>`), not surprises. New event kinds / new spec versions become *compile errors* in every dispatcher, not silent fallthroughs. Standards-grade IntentSpec relies on this — the format's predicate-subset depends on total functions. |
| 20 | **Throw-only-typed-errors** (concretised #19) | ✅ | Custom ESLint rule `tallyseal/throw-only-typed-errors`. Throws of bare values / strings / objects rejected at lint time. | Errors are inspectable, catch-pattern-matchable, audit-bundle-renderable typed instances; bare-value throws break replayability + audit-bundle reconstruction. |
| 21 | **Fast-lane pre-commit hygiene** | ✅ | `.husky/pre-commit` detects doc-only staged changes (`.md`, `.txt`, `.gitignore`, `LICENSE`, `CHANGELOG.md`, `README.md`) and runs prettier-only (~0.5s) on those. Code changes get full prettier + lint + typecheck (~10-15s). | Trivial doc fixes don't pay the full-pipeline tax; non-trivial changes still get the full gate; signal-clarity preserved via path-pattern detection. |
| 22 | **Post-commit async test safety net** | ✅ | `.husky/post-commit` spawns `pnpm test` in the background after every commit (full lane OR fast lane); prints `❌ ... consider git revert HEAD` if tests fail. Skipped during merges / rebases / cherry-picks to avoid noise. | Fast lane's speed risk is offset by post-hoc verification: any commit that broke tests (incl. trivial doc fixes that referenced moved files, etc.) surfaces immediately. CI on push is the ultimate safety net. |
| 23 | **CRAWCUS spec stays self-contained + brand-neutral** | ✅ | The CRAWCUS open-spec content (types, schemas, pure evaluators, hash chain, canonical-JSON, Contract algorithm, compliance manifest schema, readiness predicate) lives in **its own workspace package** at `packages/crawcus-spec/` (`@tallyseal/crawcus-spec`). The package has NO `@tallyseal/*` dependencies, so the TypeScript compiler structurally enforces that spec code cannot import from Tallyseal runtime — any such import fails compilation. Runtime packages (`@tallyseal/core`, etc.) depend on `@tallyseal/crawcus-spec` via `workspace:*`; the direction is always runtime → spec, never the reverse. **Lint rules as defense-in-depth + earlier IDE feedback**: `tallyseal/no-runtime-import` (blocks any `@tallyseal/*` import inside `packages/crawcus-spec/src/`) + `tallyseal/no-brand-leak` (blocks `Tallyseal` identifier or string inside `packages/crawcus-spec/src/*` content per Y10 vendor-neutrality marker; comments exempt). **Phase-2 migrations** (originally flagged as leaks; ✅ closed 2026-05-21): `HashChainProof` moved from `ports/tx-context.ts` → `@tallyseal/crawcus-spec/event/hash-chain-proof.ts` (it's the wire-format shape any conformant runtime emits). `AuditBundle` wire-format types moved from `packages/core/src/audit-bundle/types.ts` → `@tallyseal/crawcus-spec/audit-bundle/types.ts` (the Attestation primitive's wire format; composer stays in core). `Projector` interface refactored: spec defines generic `Projector<TPayload, TCtx>` + `ProjectorBaseCtx` (brand-neutral, no port deps); Tallyseal `ProjectorCtx` narrows by adding `AIPort` + `PIIPort` via TS intersection. All three migrations preserve back-compat through `@tallyseal/core` barrel re-exports. | The CRAWCUS spec is the Y10 marker (≥3 independent CRAWCUS-conformant runtimes per `00-canon/identity.md`); a Tallyseal-coupled spec falsifies that marker on day one of external visibility. With the spec as a real workspace package, the Y1 H2 spin-out (`packages/crawcus-spec/` → `github.com/crawcus/spec` repo under `@crawcus/spec` scope, per decision-log B1.3b) is a **single-step scope rename** — the package boundary already exists; the compiler refuses any drift in the meantime. Every primitive sprint that lands without the boundary enforced would compound drift; this rule eliminates the drift surface entirely. |

## The ratchet artifact

`docs/RATCHET.md` lists current values, updated weekly:

```
mutation score:          84% (target: ≥80%)
eval pass-rate:          96.2% (last release: 96.0%)
branch lifetime p95:     3.2 days (target: <5)
ratchet-exempt count:    7 (last release: 7 — flat)
p99 latency:             340ms (target: <500ms)
SBOM new transitive:     2 (reviewed + approved)
test coverage:           87% (target: ≥80%)
```

**Numbers can only move one way.** If they move the wrong way, that's a P0 process incident, not a metric to ignore.

## What this rules out

- "Just this once" exemptions to type strictness
- "We'll add tests later"
- Long-lived feature branches
- Production access without audit trail
- Skipping postmortem on a "small" incident
- Merging without threat model on IntentSpec changes
- Approving SBOM diffs without reading them
- Direct `prisma.X.create|update|delete` from `lib/witness/**` — even
  "just for this one migration"
- Non-conventional commit messages — even for trivial chores
- Branch names without date suffix when parallel sessions exist
- Skipping the PATCH bump on a docs-only or chore-only PR
- Editing from the repo root when another Claude Code session is open
- `--no-verify` to skip a failing hook (fix the underlying issue)

## What this requires from the founder

- **Hire the first compliance officer in Months 0-3.** They author regulation modules, recruit advisory board, build auditor relationships. Most technical founders skip this; doing so kills the moat.
- **Hire the first SRE in Month 4-6.** They own the observability budget + break-glass + uptime ratchet.
- **Code review discipline:** 100% PR review, no exceptions, no founder bypass.

## Process > policy

These disciplines work because they're **structural** — encoded in CI, hooks, build scripts — not because they're written in a handbook nobody reads. Anything that depends on employee compliance will erode under deadline pressure. Anything enforced by the build cannot.
