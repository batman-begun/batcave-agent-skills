# SOFTWARE CONTROLS

**Architecture:** `skills/` source → `scripts/registry_core.py` parser/validator → `scripts/build_catalog.py` deterministic JSON → consumers. CI checks catalog consistency and unit tests; no remote network requirement.

**Dependencies:** Python 3.9+ stdlib, GitHub Actions Python 3.12 for CI. `SKILL.md` root frontmatter parser supports single-line `name` and `description` (quoted or unquoted), and deliberately rejects multiline description in this v0 scaffold. It does not implement full YAML parsing; a later compatible YAML parser may replace it with tests.

**Source hygiene:** Keep secrets and private skill bundles out of public tree. No automated publishing or artifact execution. Registry discovery is read-only. PR-based review and branch protection recommended (not configured in this scaffold).

**Security limits:** No automatic secret scanning, virus scanning, legal/licensing judgment or full supply-chain proof. A passing validator only checks layout/metadata/catalog integrity.
