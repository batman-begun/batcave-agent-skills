# Batcave Agent Skills — Universal Public Registry

**Status:** Active public skill registry. Published skills are listed below.

A portable, publicly readable registry of reusable skills for AI agents. **Discovery first; compatibility and installation are separate questions.**

- [Machine-readable catalog](catalog.json) — automatically generated from approved skills.
- [Skill directory](skills/README.md) — each released skill lives at `skills/<slug>/SKILL.md`.
- [Agent instructions](AGENTS.md) — safe navigation and editing.
- [Governance](knowledge/CONSTRAINTS.md) — publication gates and source-of-truth rules.
- [Current status](state/STATUS.md) — observed state and next action.
- [Tests and validation](verification/SOFTWARE.md) — run before publishing.

## Published skills

- [`coding-agents-collab-contributor`](skills/coding-agents-collab-contributor/SKILL.md)
- [`coding-agents-collab-leader`](skills/coding-agents-collab-leader/SKILL.md)
- [`hallmark-web-design`](skills/hallmark-web-design/SKILL.md)
- [`hanyu-visual-lab`](skills/hanyu-visual-lab/SKILL.md)
- [`klein-explorer`](skills/klein-explorer/SKILL.md)
- [`universal-project-repository`](skills/universal-project-repository/SKILL.md)
- [`wonderanime-gouache-grungecel-image`](skills/wonderanime-gouache-grungecel-image/SKILL.md)

## Discover and load

Read [catalog.json](catalog.json) on `main` for the current inventory. If your reader cannot follow GitHub file links, use the [raw JSON catalog](https://raw.githubusercontent.com/batman-begun/batcave-agent-skills/main/catalog.json). Each entry points to the corresponding `SKILL.md`, which uses the [Agent Skills](https://agentskills.io/specification) convention.

Hermes supports `skills/`-based GitHub taps, for example:

```bash
hermes skills tap add batman-begun/batcave-agent-skills
```

This registers a source; it is **not** proof that any listed skill works on a given agent. See each skill's requirements and safety notes before running bundled scripts.

## Developer workflow

```bash
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
python3 -m unittest discover -s tests -v
```

The catalog is generated. Edit `SKILL.md` and optional `skill.meta.json`, not `catalog.json` by hand. Public publication requires approval and a privacy/license review before committing. See [CONSTRAINTS](knowledge/CONSTRAINTS.md).

## Release & licensing

The owner has not yet chosen a repository license. Public visibility does **not** grant unrestricted reuse rights. Each released skill must have an explicit rights/redistribution review and a documented license or permission terms before publication.

## Governance

The repository follows Universal Project Repository (UPR/1) Standard Tier, with software and knowledge profiles. The native `skills/` layout is preserved for interoperability rather than introducing a generic workspace wrapper.
