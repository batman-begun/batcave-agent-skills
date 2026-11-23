# Mandatory software engineering floor — UPR/1

## Purpose
A software profile is a strict superset of the universal core, not a generic knowledge folder. It preserves original Universal Repository Architecture objectives: independently resumable codebase, explicit architecture, constrained changes, verification, evidence, safe delivery and recovery. The skill itself is an instruction/scaffold layer, not a complete execution harness or guarantee of correctness.

## Mandatory obligations at every size
Each obligation has a named canonical location, owner or accountable role, current status, verification method and gap. Scale mechanism to risk; never omit the obligation. A one-file local script can use one document and a smoke test. A public multi-user app requires actual authorization/data isolation tests and externally enforced gates before production. Do not claim controls are enforced merely because a policy file exists.

| Obligation | Required content / proof |
|---|---|
| Intent and contract | current requirements, acceptance criteria IDs, non-goals, approved changes, behavior/invariants that can be tested |
| Architecture | logical modules/components, boundaries, dependency direction, data/control flows, external services, trust boundaries, integration contracts, rationale; actual repository paths |
| Build reproducibility | runtime/tool versions, dependencies and appropriate lockfiles, clean setup/build/run/test commands, environment example without secrets |
| Source hygiene | conventional native directories, tooling config, ignore rules, duplicate/dead code detection where justified, generated vs source distinction |
| Change control | task scope, affected modules/interfaces, migration impact, diff and tests, preservation of unrelated work; protected rules and reviewer independence where available |
| Verification | executable tests for critical invariants, regression tests, negative/error cases; static/lint/type checks if applicable; security and dependency checks; explicit skipped/not applicable reasons |
| Operations | deployment target and access policy, data handling, configuration, observability, backup/restore and rollback paths, health checks; genuinely local scripts can document local recovery |
| Evidence | revision or snapshot, exact executed commands, exit status, critical test outcomes, failure details, reproducible UAT evidence, known blind spots |

Recommended mappings: src/ or framework-native app/, tests/, docs/architecture/, docs/requirements/, docs/decisions/, harness/ (constraints/scripts), CI provider-native config, verification/ (reports/evidence pointers). Use existing equivalents rather than forcing relocations. `harness/CONTROLS.md` and `verification/SOFTWARE.md` are scaffold defaults, not substitutes for real gates. Protect review and deployment policies outside builder write authority (branch rules, restricted credentials, trusted CI configuration, required checks, independent approval). If unsupported, mark NOT ENFORCED and do not claim gate strength.

## Proportionality in lite and micro tiers
The obligations table applies at every tier; only the mechanism shrinks. In lite, the eight obligations live as the "SOFTWARE CONTROLS" and "SOFTWARE VERIFICATION" sections of `STATE.md`. Example for a one-file local utility: contract = 3 lines of acceptance criteria; architecture = "single module, no network"; build = interpreter version + run command; verification = one deterministic smoke test with its exit code; operations = local recovery ("delete output file, rerun"); evidence = the executed command and result. A section may say NOT APPLICABLE with a reason; it may not be absent.

## Risk classification and delivery
Local/offline low consequence: deterministic unit/smoke test with fixtures, run on clean environment if possible, error handling, reversible file writes, check dependencies; manual rollback documented.
Public or multi-user: additionally test authN/authZ, tenant boundaries, input validation, rate/resource limits, secrets exposure, dependency risks, data migration and rollback, accessibility/performance as relevant, integration and end-to-end flows. Verify realistic failure paths and monitoring. Production credentials isolated from testbed. Never use real private data in publicly accessible UAT; sanitize fixtures. Use protected production branch and release gate when host supports it.
High consequence (financial execution, sensitive health data, critical infra, etc.): human expert review, threat model, independent test/evidence, recovery drill, explicit release authorization and applicable compliance. AI review or owner UAT alone is inadequate. If capability absent, block production release, not safe local prototyping.

## Gate design (actual executable commands, not examples passed off as implemented)
G0 intent/design: current scope, acceptance IDs, decision conflicts resolved, independent design critique if feasible.
G1 build: clean build, dependency checks, lint/type checks, relevant architecture rules, scoped diff. Prohibit unauthorized dependency direction, oversized/duplicate patterns as applicable; avoid arbitrary metrics as sole quality measure.
G2 behavior: unit/integration/E2E/negative tests for critical contracts; reviewer-created tests from approved criteria, not merely builder examples; reproducible results tied to exact revision. Where suitable formal/property verification states assumptions and model–implementation relationship.
G3 risk/review: threat checks, regressions, unresolved severity, reviewer independence. No builder self-waiver of critical controls. Investigate conflicts, do not majority vote blindly.
G4 delivery: staging/live testbed identified and isolated, rollback/backup plan tested proportional to risk, UAT owner acceptance, authorized deployment. Preview release is not production acceptance. Verify deployed version matches reviewed revision, observe health.

Gate status vocabulary: NOT CONFIGURED, CONFIGURED (not run), PASS, FAIL, SKIPPED (reason), NOT APPLICABLE (reason), ENFORCED (describe outside-builder control separately). A failed critical gate blocks release; noncritical deferrals need explicit authorized exception and tracked remediation. CI running tests is not automatically a required protected gate. Keep gate evidence in trusted CI or read-only artifact storage where possible and link to versioned records. The builder must not change verifier or thresholds to make its PR pass without independent review.

## Anti-drift and maintainability
At each material change, check against architecture and acceptance IDs, existing reusable components, dependency cycles, duplication, complexity, dead paths, configuration drift and migrations. Use domain-appropriate static analysis plus reviewer/behavioral evidence; trend actionable metrics over time, not LOC superstition. Add regression tests for confirmed defects. Periodically audit drift of docs versus implementation. Prefer simpler local changes unless architecture decision authorizes wider refactor. Preserve change rationale and alternatives. Retain explainability: a new agent and owner at system level can trace feature→contract→component→evidence→revision; humans need not read all source, but source and recovery remain accessible.

## Verification reporting
Include exact commands + exit codes, execution environment, target revision, result, artifact path, coverage limitations, last known deploy identity, open risks, human acceptance status. Report actual checks, not generic test claims. A test pass proves sampled behavior, not universal correctness; formal proof proves a statement under assumptions, not completeness of business intent. UPR structural check is only G0 navigation hygiene, not G1–G4. Never label scaffolding production-ready.
