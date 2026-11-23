# Textless art generation and provider adapter

## Separation of responsibilities

**Agent** calls its native image generation tool or connected external provider. The local Python compositor never sends requests to a commercial API and never accesses authentication tokens. Provider API billing, quotas, rate limits and provider availability are runtime-specific. Do not assume any subscription funds another provider.

**Illustration contract** for one tile:
- Input: an English visual brief explaining the meaning of one phrase, plus series-wide style canon
- Output: a single PNG/WebP/JPEG with an isolated, coherent kawaii illustration, no letters, numerals, text, logos, UI labels or watermark
- Style: same brown-haired double-bun pink-hoodie chibi protagonist, thick ink outlines, pastel, recognizable everyday props
- Composition: subject centered, safe margin 8%, light/simple or transparent background, no text at any location
- Storage path: `assets/illustrations/<item-id>.png`
- The image's **index** is assigned externally from its filename; never rely on image model's ability to print an item number in the drawing

## Recommended generation methods

**Best quality:** one illustration per item or small groups with external identity control. More calls, accurate scene mapping.

**Low-cost option:** a textless uniform **NxM art sheet** with equal-sized cells, one scene per item, no labels or borders; crop cells using code, save as `01.png` etc. The agent verifies scene-to-cell mapping manually; if mixed up, selectively regenerate individual tiles. Avoid tiny dense sheets (20 scenes in one low-resolution picture can lose expressive detail).

**Fallback:** if the selected provider cannot draw transparent art, request simple pale background and let the card frame visually absorb it. If provider fails entirely, vector placeholders work for a typographic layout preview only, **not for final illustrated publishing**.

## Style anchor prompt

> Cute kawaii Chinese-learning educational illustration, consistent girl with light brown hair in two symmetrical buns, pink bunny hoodie, warm rosy cheeks, vivid expressive face, outlined pastel cartoon with subtle texture, coherent cozy lighting, clean isolated vignette, generous negative space, no letters, no words, no alphabet, no Chinese characters, no labels, no numbers, no UI screenshots, no watermarks. Scene: [specific visual brief]. Landscape card vignette with safe margins.

When reusing a user-supplied illustration as inspiration, do not copy existing graphic text into new art. Reuse authorized style references as visual references only.

## Art coverage

The renderer will work with missing images, using a deliberately simple abstract heart/sparkle placeholder to demonstrate text positioning. Before final publication, verify illustration coverage (number of valid art files / total cards) and screenshot content. Never present a fallback-only poster as if image generation succeeded.
