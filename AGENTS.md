# Agent entrypoint

Read in order: `README.md` → `PROJECT.json` → `state/STATUS.md` → `knowledge/CONSTRAINTS.md`. For skill discovery, read [catalog.json](catalog.json) on `main` and load only the selected entrypoint and its supporting files. If the catalog cannot be fetched, the README lists direct skill entrypoints.

This public repository is for discoverable, approved skills. Do not import a Library archive, private files, credentials, personal memories, external links with tokens, or copyrighted third-party assets directly into `skills/`.

Every skill must live at `skills/<slug>/SKILL.md` with valid Agent Skills frontmatter (`name`, `description`) and matching `name`. `skill.meta.json` extends registry discovery only; it is not part of the Agent Skills standard. Generate catalog with `python3 scripts/build_catalog.py`, run tests, and review a staged diff before any push. No agent may self-approve publication. Use a feature branch/PR for proposed skill additions.

The canonical content of a skill is its `SKILL.md` and bundled files. `catalog.json` is generated discovery metadata, never an alternate instruction source. User/owner approval applies to a specific public snapshot, not all future changes.
