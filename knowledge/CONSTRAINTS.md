# CONSTRAINTS

- **CON-001 — Public content gate:** No files from personal Library, old ZIPs or private repos become public merely because they exist. A named owner approval of publication scope is required. Review source, linked docs, sample images, metadata, license, private names, endpoints and tokens. Git history persists.
- **CON-002 — Single source:** `skills/<slug>/SKILL.md` and bundled resources are canonical; `catalog.json` is regenerated and checked in CI.
- **CON-003 — Portable shape:** Skill folder equals the `name` field in SKILL.md. Avoid platform-specific paths in core instructions; platform adapters may be separate.
- **CON-004 — Discovery != execution:** Catalog visibility does not imply that a consumer has required permissions, runtimes or tools.
- **CON-005 — Supply-chain awareness:** A skill can contain commands/scripts. Document dependencies, network/security implications, scopes, asset rights and runtime constraints; read and review before execution.
- **CON-006 — Authority:** An agent cannot self-approve publication, waive security checks or change owner-approved constraints. Public commits are not equivalent to owner approval of content.
- **CON-007 — License:** Don't invent permission to redistribute existing skills or art assets. Repository-level license must be explicitly decided by owner; per-skill third-party licenses remain binding.
- **CON-008 — Separation:** Private staging stays outside public Git, e.g. ChatGPT Library or private repo. Public GitHub can reference private content only through non-sensitive generic documentation.
