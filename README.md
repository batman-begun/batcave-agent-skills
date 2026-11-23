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
- [`ffmpeg-motion-director`](skills/ffmpeg-motion-director/SKILL.md) — image-to-video direction with 15 FX and a bundled FFmpeg renderer.
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

## Licensing

The Batcave-owned registry scaffolding, generator, schema, tests, CI, and repository-level documentation are available under the [MIT License](LICENSE). The catalog is an index. Each package under `skills/` specifies its own licensing scope.

- The published skill packages have MIT terms for the Batcave contributions identified in their individual `LICENSE` files.
- Hallmark Web Design retains the [upstream MIT notice](skills/hallmark-web-design/LICENSE.upstream) for material from Nutlope/Hallmark.
- WonderAnime's MIT grant covers its written material. Its visual reference and near-miss image sets remain private and have no public license grant.
- External materials and future assets follow their own terms.


## Governance

The repository follows Universal Project Repository (UPR/1) Standard Tier, with software and knowledge profiles. The native `skills/` layout is preserved for interoperability rather than introducing a generic workspace wrapper.
