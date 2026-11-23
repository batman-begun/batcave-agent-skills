# Published skills

Every **approved** public skill belongs in `skills/<slug>/SKILL.md` and optional `scripts/`, `references/`, `assets/`. Do not copy archive ZIPs to the public tree. Extract, normalize, review, test and license each one before publication.

Optional additional registry information can be placed in `skill.meta.json` alongside `SKILL.md`:

```json
{
  "version": "1.0.0",
  "category": "design",
  "tags": ["infographic", "education"],
  "runtime_requirements": ["python>=3.9", "image_generation"],
  "compatibility": ["unknown"],
  "license": "LICENSE-file-or-identifier"
}
```

These fields are **registry-specific**, not Agent Skills standard fields. Required standard frontmatter in SKILL.md: `name`, `description`. Keep them concise and actionable. Don't claim tested compatibility without evidence.
