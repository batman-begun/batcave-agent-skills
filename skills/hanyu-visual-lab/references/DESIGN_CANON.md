# HanYu Visual Lab — visual design canon

## Fixed art direction

- **Canvas:** landscape 4:3; browser viewport 1600×1200; final screenshot 3200×2400 at 2× device scale.
- **Character:** one recurring expressive brown-haired chibi girl, two small buns, rosy cheeks, pink hoodie with simple rabbit motif. Supporting people/animals only when semantically justified. No resemblance claims to real individuals.
- **Style:** playful thick-line kawaii, rounded geometry, soft gradients, pastel sky blue, spring green, lavender, rose and gold; richly illustrated but white space around text.
- **Decor:** wooden title sign, pink subtitle ribbon, hearts/music notes/sparkles/plants only where they do not compete with text.
- **Cards:** section header colored to match group, each expression in a rounded tile with the Hanzi first, Pinyin next, Vietnamese meaning last; illustration in its own region beneath/adjacent.
- **Memory strip:** 6–8 existing anchor phrases reused from lesson, not a separate set of unverified new text.

## Design rules

1. Text zones are created **by code before art placement**; the image model receives illustration-only instructions.
2. Do not let generated art occupy the same zones as text. A model that draws text accidentally gets rejected or cropped/retried.
3. Prefer 3–5 sections with 4–6 items each, but a 2-section lesson may be appropriate for short inputs.
4. Chinese should be the largest type; Pinyin smaller, still clearly readable; Vietnamese visibly distinct. Font minimums in renderer are enforced via DOM checks. Exact glyph rendering depends on installed fonts.
5. Group by communicative context, not arbitrary taxonomy. In Data Mode, every input appears exactly once outside the memory strip.
6. A poster with too many long phrases is **split**, not crammed at microscopic font sizes.
7. Character consistency matters more than intricate backgrounds. Keep illustrations legible at card-scale rather than cinematic wide shots.
8. Always inspect the exported image visually. Text checks do not guarantee natural layout or accurate art.

## Layout availability note

The reference planner recognizes vocabulary, grammar and dialogue narratives. The included **v1 renderer implements the vocabulary-section card template**, which can host phrase or short-sentence content; specialized dialogue/sentence-comparison templates should be built as an enhancement rather than misrepresented as available now.
