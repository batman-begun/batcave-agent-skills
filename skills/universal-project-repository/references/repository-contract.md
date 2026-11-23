# UPR/1 repository contract

## Core layout and tiers
Every tier has a root README.md and one manifest (`PROJECT.json`, or legacy `PROJECT.yaml`; exactly one). `AGENTS.md` is required above lite. Role paths are a logical interface, not mandatory directory names. Relative normalized paths only, no symlinks to external/private areas for role mapping. Native layouts have precedence over cosmetic uniformity. All eight roles must be explicitly mapped to existing files/directories; tiny projects may co-locate roles with labeled sections.

| Tier | Appropriate | Minimum |
|---|---|---|
| lite (default) | new or small project, one owner, one session or few | `README.md`, `PROJECT.json`, `STATE.md` with one labeled section per role (plus software controls/verification sections if software) |
| micro | small project needing separate agent navigation or artifact index | root docs + AGENTS.md + manifest + a consolidated project record and artifact home; software floor still applies if software |
| standard | ongoing creative or product project | separate current intent, knowledge, constraints, state, decisions, artifacts, evidence; focused indexes |
| extended | multi-component or high risk | component scope/indexes, decision and risk registers, evidence/approval policy, release and recovery plans, isolation and cross-project boundaries |

Choose by complexity, collaboration and consequence, not line count alone. Choose the appropriate tier directly. Use standard or extended for public or multi-user software. Reassess as risk, collaboration or canon grows and record why. Do not make empty folders or blank files just to look complete; starter placeholders are allowed, explicitly marked, and prevent a readiness claim. Do not create duplicate canonical documents. For multiple profiles use scoped indexes and document which profile applies to which component.

Suggested standard mapping (paths are defaults, not a migration mandate):
```
README.md
AGENTS.md
PROJECT.json              # or PROJECT.yaml (legacy), never both
intent/INTENT.md
intent/CONTEXT.md
knowledge/INDEX.md
knowledge/CONSTRAINTS.md
state/STATUS.md
workspace/INDEX.md        # domain-specific artifacts may instead be src/, manuscripts/, etc.
verification/INDEX.md
history/DECISIONS.md
decisions/                # optional individual ADRs, indexed from history/DECISIONS.md
artifacts/                # optional manifest/releases; no duplicate working artifacts
research/                 # optional source/experiment records
harness/                  # software rules, executable checks, planned controls distinguished
```
Never infer that directory names alone enforce policy. Git need not track external assets; role paths point to versioned manifests.

## Manifest
`PROJECT.json` is plain JSON (valid YAML 1.2). Legacy `PROJECT.yaml` is accepted only if its content is also JSON; the bundled checker accepts this portable subset only, with no external dependencies, and rejects a project that has both files. Other YAML styles require a compatible alternative checker or explicit conversion with owner approval. Required fields (tier is one of lite, micro, standard, extended):
```
{
  "schema": "upr/1",
  "project_id": "example",
  "title": "Example",
  "profiles": ["software"],
  "tier": "standard",
  "lifecycle": "active",
  "visibility": "local",
  "roles": {
    "intent": "intent/INTENT.md", "context": "intent/CONTEXT.md",
    "knowledge": "knowledge/INDEX.md", "constraints": "knowledge/CONSTRAINTS.md",
    "state": "state/STATUS.md", "artifacts": "workspace/INDEX.md",
    "verification": "verification/INDEX.md", "evolution": "history/DECISIONS.md"
  },
  "software": {"controls": "harness/CONTROLS.md", "verification": "verification/SOFTWARE.md"}
}
```
ID lowercase stable slug. Profiles: software, novel, comic, science, philosophy, contemplation, business, knowledge, custom. lifecycle: proposed, active, paused, archived, completed. Visibility: local, private, internal, public (declared target, not proof of remote ACL). Software references are mandatory when software selected; actual software root may stay native. Written by the scaffold: `skill_version`. Optional: owner reference (avoid personal PII), `profile_scopes`, `upstream`, `related_projects`, `asset_manifest`, `authority_policy`. The checker validates basic structure only, not optional semantics. Changing schema version requires compatibility review; do not silently rewrite manifests.

## Human and agent interfaces
README: purpose, current stage, first thing to read or try, links to the authoritative project records, and any relevant visibility or usage limits. AGENTS: concise map, load order, governing documents, applicable profile(s), do-not-do rules, how to verify/checkpoint, context separation; prefer links and local module instruction maps to dumping full history. State: last observed baseline, in-progress and next actions, open decisions, evidence gaps, revision/time if known. If code has changed since status, report stale state and reconcile. Do not imply a commit includes its own hash: record prior verified baseline, or attach evidence after commit in another record.

## Public-facing README and showcase

Lead with what the intended reader needs to understand or try. When a representative result is ready and approved for the audience, feature it and link to the exact source revision or versioned input, relevant evidence, and a way to reproduce, inspect or challenge the result. Put compact examples inline. Link to a separate case page when readers need more room for evidence, walkthroughs or media. If the project is early, state the stage and point to the best approved starting material.

Keep showcase claims within the scope of the cited evidence. Use the existing artifact and verification records as sources and link to them. The role map already covers those records. Choose presentation format by domain and reuse the native repository layout.

## Authority model
1. Applicable host/safety rules; explicit authorized owner decision and scope.
2. Current approved intent, constraints and designated domain canonical docs; resolve contradictory approved sources explicitly.
3. Observations and artifacts establish what exists, not what should exist.
4. Working proposals, source notes, raw story, prior discussions and reviewer findings supply context, not authority. Historical superseded records never silently revive.
Use stable IDs e.g. INT-001, REQ-014, ADR-003, CAN-012, OBS-023, HYP-004, EVD-008. Link claims to source/revision and evidence. Domain-specific IDs are fine. Maintain current pointers not replicated copies. Decision status separate from epistemic strength; owner approval cannot turn a hypothesis into scientific truth.

Lifecycle proposed→active→paused/completed→archived (reopen explicitly); never delete merely because archived. Branches may explore alternatives, not silently redefine approved baseline. Mark experimental branch artifacts clearly. Merge approval and product approval are separate. Checkpoint at meaningful progress/evidence boundaries; record next action. Keep source record history when safe, but privacy obligations override archival preference.

## Which status vocabulary for what
Use exactly one vocabulary per question; do not mix.

| Question | Vocabulary |
|---|---|
| Is this decision/spec accepted? | DRAFT, PROPOSED, APPROVED, SUPERSEDED, REJECTED |
| How strong is this claim? | observation, hypothesis, inference, fiction, source-reported, verified-within-scope |
| Is a software control in place? | NOT CONFIGURED, CONFIGURED (not run), PASS, FAIL, SKIPPED, NOT APPLICABLE, ENFORCED |
| Did an evaluated criterion/review pass? | PASS, FAIL, INCONCLUSIVE, NOT_RUN |
| How ready is the project? | SCAFFOLDED, DOCUMENTED, VERIFIED, RELEASE-READY |
| Audit coverage of a requirement | PRESENT, PARTIAL, MISSING, NOT APPLICABLE |

## Lint strictness
`check` is lenient by default (placeholders are warnings, so a fresh scaffold is "structurally OK"). Use `check --strict` where it gates anything (CI, handoff, "done" reports): placeholders, empty or unreadable mapped record files, and missing or empty required sections in shared lite records become errors. Strict still only proves structure, never substance.
