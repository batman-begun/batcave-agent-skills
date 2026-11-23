---
name: hallmark-web-design
description: Use Hallmark Web Design when asked to design distinctive websites or interfaces, audit UI for generic AI-design patterns, or explicitly redesign an existing site while preserving functionality. Also trigger for Hallmark and anti-AI-slop design requests; do not silently redesign existing products.
---

# Hallmark Web Design — source-connected Hallmark v2

**Status:** This is a portable, source-connected adapter, **NOT a full offline copy of Nutlope/Hallmark**. The bundled 50-theme *catalog* is complete for upstream commit `04977e15f3dfd6ee4b74c887dac3eb52665d6c92`, but the 50 individual Markdown definitions, 50 `.jpg` previews, 187 upstream payload files, and browser-executable scripts are NOT bundled in this plugin archive. Do not pretend they are present or that SlopLint ran. This limitation must remain explicit during export.

Upstream: https://github.com/Nutlope/hallmark · MIT, copyright (c) 2026 Hallmark contributors. Source pin: `04977e15f3dfd6ee4b74c887dac3eb52665d6c92` (2026-11-11). `references/themes-catalog.md` provides the complete 50-entry *navigation index* (not full themes). `references/upstream-parity.md` identifies what to load and how to verify parity.

## Modes

- `design <brief>`: a new site/page. Read upstream `SKILL.md`, relevant references and one selected theme before applying. Start with the user's real audience, job, core action, evidence and brand constraints. Never fabricate metrics, testimonials or logo walls. If the user says "custom", use upstream `references/direction.md`, do not force a named theme.
- `audit <target>`: **read-only**. Examine actual available code, screenshots, URLs, accessibility and responsiveness. Prefer runtime SlopLint where executable. Report observed vs inferred problems separately; never edit in audit mode.
- `redesign <target>`: only on explicit command; establish baselines for route/link inventory, fields, handlers, content, i18n, admin/auth, metadata and analytics. Preserve existing design canon unless user explicitly overrides. Run before/after preservation tests where executable.
- `quality gate`: Floor = non-waivable functional/a11y/contrast/safety/responsive failures, Reflex = default AI design tells with documented exceptions, Finish = nonblocking polish. Treat warnings and verified failures differently.

## Pinned upstream source

For any real Hallmark task **when GitHub access is available**, read the original upstream files with any available GitHub file tool or verified local checkout for repo `Nutlope/hallmark`, `ref` set to commit `04977e15f3dfd6ee4b74c887dac3eb52665d6c92` (or explicitly inspect a newer commit before changing pin):

1. Read `skills/hallmark/SKILL.md` (the authoritative upstream skill; never replace it with the adapter's condensed summary).
2. Read `skills/hallmark/references/themes/index.json` to select among 50 themes based on user intent (genre, keywords, postures), or use bundled index if GitHub is unreachable.
3. Read relevant upstream reference files by exact path, e.g. `skills/hallmark/references/gates.md`, `flow.md`, `redesign.md`, `layout.md`, `responsive.md`, `review-hero.md`, `review-finish.md`, and `direction.md` as the upstream skill instructs. Do not claim to have read a file until fetched.
4. Fetch the **full chosen theme** at `skills/hallmark/references/themes/<slug>.md` before using it to design. Its `.jpg` sibling is optional visual context; do not claim it was visually inspected unless actually viewed. Do not flatten themes into fixed page templates.
5. For any code run or QA report, use the original `skills/hallmark/scripts/theme.mjs`, `sloplint.mjs`, `sloplint-render.mjs`, and other required scripts **in an authorized local runtime**; do not claim runnable source is in this adapter package.

If neither GitHub nor a verified checkout is available, use bundled `references/themes-catalog.md` for orientation, report this as **degraded mode**, and do NOT claim upstream-complete behavior.

## Safeguards

- Read `design.md` or approved design canon first; user's live design decisions outrank generative theme suggestions.
- Never silently remove routes, forms, authentication, admin entry points, comments, i18n, SEO, or existing behavior to make a layout prettier.
- Preserve accessible keyboard focus, reduced-motion paths, tokens, truthful copy, semantic HTML, flexible text wrapping and real mobile testing.
- Perform independent review when possible; the agent that built the page should not be the sole reviewer.
- Never run unreviewed third-party code. Cite upstream and pin the revision when generating assets or attributing borrowed patterns.
- Source-retrieval is **not** equivalent to code execution. Static QA is not browser QA.

## Offline/full-source export to OpenCode, T3-DGR, Codex

Use bundled `scripts/bootstrap-full-hallmark.sh` on the **user's local machine** to fetch the complete upstream repo at the pinned commit and install `skills/hallmark` into the OpenCode agent skills path, after inspecting it. The script refuses to overwrite existing targets. Requires Git, internet access, Python 3 for validation; Node 18+ and Chrome / puppeteer-core are required for original runtime/browser checks. The source is fetched at execution time; it is **not embedded in this package**.

The adapter may travel with the complete upstream `skills/hallmark/` folder after a local bootstrap, but preserve upstream files and put custom overrides separately. Do not call the ZIP "offline full-source" until that folder is actually present and validated.
