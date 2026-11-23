# UPR workflows (read only the section you need)

Contents: Classify · INIT · RESUME · CHECKPOINT · AUDIT/MIGRATE · REVIEW-PACKET · PORTFOLIO

## Classify
Match scope and permissions to the task: INIT, RESUME, CHECKPOINT, AUDIT, MIGRATE, REVIEW-PACKET or PORTFOLIO. Apply UPR at project inception (even before code or artifacts exist), when adopting an existing repo, at substantial handoffs, and when auditing structure. For a small ephemeral answer, do not create a repo unasked. Honor explicit standing permissions within their scope. Mixed domains inherit the union of applicable profile requirements.

## INIT
1. Inspect location, tools, size, risk, domain, intent and privacy. Reuse an existing repo when appropriate; avoid duplicate sources of truth. If enough is known, proceed with documented assumptions; unresolved sensitive or irreversible choices stay blocked. Pick profile(s) and tier based on the intake rules in SKILL.md. Default to private/local.
2. Establish project identity, the role map and the current intent baseline. Keep raw story separate from approved truth. Mark unknowns; never promote an agent guess to canon. Use `assets/record-templates.md` and `repository-contract.md`.
3. Scaffold the smallest honest structure. Keep native layouts (`src/`, `chapters/`, `notebooks/`…); do not wrap working software in `workspace/` to satisfy a tree. Optional: `python scripts/upr.py init TARGET --id ID --title TITLE --profiles software,knowledge [--tier lite|micro|standard|extended]` as a dry-run, then `--apply` only for authorized local writes. The script writes placeholders only; no Git or network action.
4. Apply every chosen profile's obligations and write real verification commands or manual protocols. For software, implement actual guards where feasible and distinguish configured, executed, enforced, unavailable and pending. Where evidence cannot be gathered, say so.
5. Run `python scripts/upr.py check TARGET` (and `--strict` once populated). Fix structural errors; review warnings. Verify role maps, authority, privacy and substantive quality separately. Commit or push only if permitted, and record the actual revision once known.

## RESUME
1. Read applicable repository instructions first, then `PROJECT.json`/`PROJECT.yaml`, state and current intent. Capture branch/revision or snapshot identity. Check for dirty work, conflicts, stale pointers, concurrent actors. Do not overwrite user changes.
2. Load only the relevant approved knowledge, constraints and profile instructions. Inspect actual artifacts and prior evidence as needed. Load history on demand to answer "why", not wholesale. Reconcile recorded state against the observable repo and note discrepancies.
3. Restate the scoped task and acceptance criteria; identify gates and unknowns. Make no unilateral change to locked intent/canon, safety rules or unrelated components.
4. At substantive boundaries run CHECKPOINT; never end a material build with only chat memory.

## CHECKPOINT
Record what changed and why; actual revision or artifact IDs; tests and reviews run with results; pending issues; approvals (or pending approval); next actionable step; impact on canon/requirements. Update current status in place; append or supersede durable decisions. Advance authoritative pointers only for justified, approved changes. Avoid duplicate summaries with divergent truth. Checkpoint at meaningful boundaries, not every turn. If file or remote tools are unavailable, return a handoff packet labeled NOT SAVED.

## AUDIT / MIGRATE
Read `migration-and-portfolio.md`. Audit read-only first; map existing evidence and role equivalents; preserve Git history and native build/publish paths; propose minimal reversible changes. Do not silently relocate files, rewrite history or clean untracked data. Migrate only with authorization; validate before and after, check downstream references, state a rollback. Report PASS / PARTIAL / BLOCKED with concrete evidence and limits.

## REVIEW-PACKET
Read `independent-review.md`. Use distinct reviewer contexts at design and artifact boundaries. Reviewers get an immutable target, approved intent/criteria, relevant evidence and necessary access, not the builder's conversation or advocacy. Prefer blind-first, sequential disclosure. A fresh session alone does not prove isolation; if isolation is unavailable, label the review CONTEXT-SHARED (non-independent). Preserve dissent. The owner decides; hard gates should execute outside builder control.

## PORTFOLIO
Read `migration-and-portfolio.md`. An optional master index repo maps projects, relations, states and shared skill versions; the child repo stays canonical. Do not embed private cross-project material in public repos. Search/indexing and orchestration are separate capabilities. Use allowlisted pointers and refresh status from authoritative sources.
