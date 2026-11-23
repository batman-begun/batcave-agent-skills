---
name: hanyu-visual-lab
description: Build one or more Chinese–Pinyin–Vietnamese kawaii educational infographic images from either a three-column vocabulary/phrase table (Data Mode) or a topic/request (Topic Mode). Plans lessons, validates language, designs textless illustrations, lays out exact multilingual typography in code, runs visual QA, and exports PNG plus editable HTML and JSON.
compatibility: Requires a coding agent with Python 3.10+, Playwright, Chromium, Chinese/Vietnamese fonts, and an optional image-generation tool or provider for chibi illustrations. Image generation is invoked by the agent; the renderer itself is offline.
metadata:
  version: "1.0.0"
  language: "zh-vi"
---

# HanYu Visual Lab — Dual-Entry Infographic Factory

**Job:** Deliver a completed, legible image infographic for Vietnamese learners of Mandarin Chinese, in a consistent kawaii-chibi design. The final educational text must come from verified structured data, **never text painted by an image model**.

## When to activate

- A user pastes Chinese expressions with **Chinese + pinyin + Vietnamese** and asks for an infographic or illustrated lesson.
- A user names a **topic or communicative situation** (e.g. “hôn nhân và gia đình”, “đi khám bệnh”, “đặt món online”) and asks the agent to design a lesson infographic.
- A user requests revisions, regenerations, or a series of posters in this visual format.

Do not use this skill for ordinary translations, quizzes, or unrelated image requests.

## Core contract

**Mode A — Data Mode (source-locked):** The input is a three-column table or numbered list. Extract all entries, preserve Hanzi, Pinyin and Vietnamese meaning, and arrange them into a lesson. Do not silently add, delete or rewrite entries. If a definite factual typo is found, create a change log and show the corrected entry; uncertain edits require review. Reordering/grouping is allowed, while the original IDs and a complete coverage ledger are retained. No new example sentences unless explicitly requested.

**Mode B — Topic Mode (model-authored):** The user provides a topic and possibly proficiency level, target phrases, or preferred size. Agent narrows it to **one natural real-life situation**, drafts an initial table of 8–16 practical Chinese expressions (12 default), generates Pinyin with tone marks and concise Vietnamese meanings, checks grammar/pronunciation, then saves the **same canonical lesson JSON** used by Data Mode. The model-authored entries are labeled `source_mode: topic`. Do not claim generated material was user-provided. For broad topics, choose a coherent subtopic or make a short series when justified; do not produce a random, disjoint 20-item list.

Both modes converge on one pipeline:

`input → normalized rows → linguistic review → inferred topic/section layout → lesson.json → textless art → code compositor → automated QA → PNG + HTML + QA report`

## Execution — always do these steps

1. **Detect mode.** If input includes identifiable Hanzi–Pinyin–Vietnamese triplets, choose Data Mode; else if user requests a lesson by topic, choose Topic Mode. If partial table, preserve rows and ask for missing detail only if essential; do not turn partial tables into Topic Mode without authorization.
2. **Parse input.** For CSV/TSV/pipe/JSON, run `python scripts/render.py import FILE --output staging.json`. For freeform numbered lines, do structured extraction yourself into JSON first; word boundaries between Pinyin and Vietnamese in unseparated text are ambiguous, so never guess solely with a naïve regex. Remove only list numbers and whitespace unless a correction is justified.
3. **Review Mandarin/Pinyin.** Inspect polyphonic characters, tone marks, sandhi, word boundaries, measure words and natural usage. Avoid fake automatic guarantees. Clearly record `corrections` and `uncertain_items`. Data Mode must be faithful to user-provided content unless the user requests edits. See [Language & content rules](references/LANGUAGE_QA.md).
4. **Plan the lesson.** Infer an umbrella context, choose a Chinese title and Vietnamese subtitle, group into 2–5 logical sections, design a memory bar with up to eight **existing** item IDs. Use 4:3 landscape. Select layout `vocabulary-clusters` unless the input naturally contains a clear step sequence or dialogue. Do not fabricate grammar examples to fill template space. See [Planner schema](references/LESSON_SCHEMA.md) and [Design canon](references/DESIGN_CANON.md).
5. **Create `lesson.json`.** IDs must be unique stable strings (e.g. `01`), every item has `hanzi`, `pinyin`, `vi`; section order follows learning logic. Preserve each Data Mode row exactly once; memory strip may repeat by ID. `source_mode` must be `data` or `topic`.
6. **Run data gate.** `python scripts/render.py validate lesson.json`. Stop and correct schema errors. If more than 20 short entries or severe density issue, split into multiple lesson files instead of shrinking text below readability. If rendering QA later fails, revise layout/split.
7. **Generate illustrations without text.** Use the available image-gen provider/tool to create one chibi scene per item or a sheet of uniform cells cropped to item ID. Text in art must be prohibited: no Chinese, Pinyin, Vietnamese, signs, labels, screen text, logos, random pseudo-writing. Source prompts from each item's **meaning and scene**, not from handwritten graphics containing words. Keep consistent art director rules in [Provider playbook](references/ART_PROVIDER.md). Save images to `assets/illustrations/01.png`, `02.png`, etc. If generation capability is absent or provider fails, renderer can produce a vector-placeholder *layout preview*, but **do not call that a complete illustrated deliverable**.
8. **Code-render typography.** Run `python scripts/render.py render lesson.json --out output`. Code places Chinese, Pinyin, Vietnamese text into actual HTML/CSS boxes and produces `output/infographic.html`, `output/infographic.png`, `output/qa.json`. It embeds all illustration images as data URIs, so the HTML remains portable. Use the exact canonical text, never OCR/retype an art image.
9. **Quality gate.** Check `qa.json`: source-text equivalence, missing/duplicate items, count, DOM overflow, minimum font sizes, text/image overlap, image coverage and visible poster appearance. Manually inspect the rendered PNG for aesthetics and Chinese/Pinyin/Vietnamese consistency. A `PASS` from code is **rendering QA only**, not a certification of linguistic accuracy or correct artwork. Replan/regenerate as needed, no silent bad results.
10. **Deliver.** Return the finished PNG, optionally the editable HTML/source JSON and QA report. State clearly when it is an unillustrated preview or if generated vocabulary still needs human language review. For several posters, name them `lesson_01`, `lesson_02` and create a ZIP.

## Defaults

- Target: Vietnamese learners of Mandarin, neutral standard Putonghua, Simplified Chinese.
- Topic Mode default: 12 expressions, beginner-to-lower-intermediate, practical utterances, concise enough for a poster.
- Data Mode: use every source expression, no rewording or invented extras by default.
- Max 20 short items per poster, fewer when sentences are long; split at 21+.
- 4:3 landscape, rendered at 3200×2400 px; Chinese visually primary; Pinyin and Vietnamese fully legible.
- 1 consistent chibi girl with brown double buns, pastel pink outfit; watercolor-like cozy kawaii cartoon, pastel blue/green/pink/purple/yellow panels, wooden header, rounded corners, playful icons.
- No external images scraped without authorization/license. Illustrations and text are separate compositing layers.

## Provider routing and budget

Try the provider explicitly requested by the user. If none, select an available image generator capable of producing consistent, textless illustration. Batch images only when scene-to-cell mapping is reliable. Never claim any particular provider's API is free or that ChatGPT Plus includes external API usage. If no provider is callable, return `lesson.json` and an honest unillustrated preview, not a fictitious finished graphic.

## Hard stop / fallback conditions

- Unclear source word boundaries: convert manually with linguistic verification, not a brittle regex.
- Inconsistent or dubious Chinese/Pinyin: flag and review before production.
- Tiny/missing glyphs, clipped text, 20+ overly long sentences: split, enlarge or re-layout.
- Bad image model typography: discard the model's text, regenerate textless art; never OCR-correct a merged poster if code can typeset it.
- Scene mismatch: regenerate only that numbered illustration without disturbing other cards.
- No image API: generate vector preview but mark art coverage missing.

## Helpful references

- [Canonical JSON schema and examples](references/LESSON_SCHEMA.md)
- [Art, typography and layout canon](references/DESIGN_CANON.md)
- [Language QA, Pinyin and authorship rules](references/LANGUAGE_QA.md)
- [Multi-provider textless illustration workflow](references/ART_PROVIDER.md)
- [Integration and usage guide](README.md)
