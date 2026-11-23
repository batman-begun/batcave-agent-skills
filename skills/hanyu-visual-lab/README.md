# HanYu Visual Lab v1 — portable Agent Skill

**Two inputs, one output engine:**

- **Data Mode:** Chinese + Pinyin + Vietnamese table → illustrated lesson infographic.
- **Topic Mode:** user topic → LLM authors a checked 3-column table → same infographic pipeline.

## What's actually implemented

- A ready-to-load `SKILL.md` for compliant coding agents.
- Detailed multimodal workflow and provider-independent image production instructions.
- Parser for clean CSV/TSV/pipe and JSON-array input; unstructured numbered lines are parsed by the calling LLM.
- Offline deterministic HTML/CSS compositor that exports 3200×2400 PNG (Playwright/Chromium) with real Chinese/Pinyin/Vietnamese typography, up to 20 cards, plus memory strip.
- Schema validation, unique-ID/coverage checks, text-node round-trip check and browser overflow QA.
- Example 20-expression lesson dataset; basic tests.

**Not yet included:** automatic calling of a proprietary image API, automatic model-based linguistic verification, an end-to-end hosted UI, or special layouts for full conversational dialogues. These are agent responsibilities or future additions. A fallback icon poster is a preview, not full chibi art.

## Requirements

Python 3.10+, `playwright`, Chromium (install via your OS package or `python -m playwright install chromium`), fonts `Noto Sans` and `Noto Sans CJK` or substitutes. The renderer auto-selects `/usr/bin/chromium` if present.

```bash
python -m pip install playwright
python -m playwright install chromium
```

## Example: Data Mode

```bash
# If source is pipe/CSV/TSV or structured array:
python scripts/render.py import examples/short-table.tsv --output staging.json
# Agent groups staging entries, adds title and section labels, writes lesson.json.
python scripts/render.py validate examples/home-leisure.json
python scripts/render.py render examples/home-leisure.json --art-root . --out output
```

`assets/illustrations/01.png` ... `20.png` will be inserted automatically if supplied. Without them, the program creates a vector-placeholder **layout preview**.

## Example: Topic Mode

Agent receives: `Làm 1 lesson: hôn nhân & gia đình; 12 cụm từ cơ bản`.

Agent creates a language-reviewed JSON with `source_mode="topic"`, 12 items, coherent subtopic and grouping; next steps are identical to Data Mode. It should not simply feed the topic string directly to the image API.

## Output files

- `output/infographic.png`: composited screenshot at 3200×2400
- `output/infographic.html`: self-contained editable code layout with embedded art
- `output/qa.json`: static input and DOM/overflow QA result
- `lesson.json`: user-supplied or generated normalized content

## Connecting to T3 Code

Place this folder where the selected coding agent reads local skills (often `.agents/skills/` in a project, with agent-specific variations), or explicitly instruct that agent to read this `SKILL.md`. T3's own picker/discovery behavior can vary by provider; verify activation empirically. This package has **not** been installed into your local T3 environment by this chat.

## Privacy and provider costs

Image generation, if available, occurs through the agent/provider tool that you configure. This package does not include credentials or transmit data independently. Generated content might incur API charges; no default provider is guaranteed free.

## Sprite sheet import (optional)

If an agent generates a **textless** 4×2 art sheet for items `01..08`, crop it into card illustrations:

```bash
python scripts/slice_art_sheet.py sheet.png --rows 2 --cols 4 --ids 01,02,03,04,05,06,07,08 --out assets/illustrations
python scripts/render.py render examples/home-leisure.json --art-root . --out output
```

Review individual crops against their phrases; correct index or regenerate mismatched tiles. Each saved file is embedded in the finished HTML and PNG.

## Publication and reuse

This package's Batcave contributions are available under [MIT](LICENSE).
