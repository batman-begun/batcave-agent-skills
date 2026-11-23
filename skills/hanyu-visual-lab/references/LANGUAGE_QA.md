# Linguistic QA policy

## Four separate gates

1. **Source preservation (deterministic).** Track all user-supplied rows and compare against structured output. Data Mode must not silently change Hanzi, Pinyin or Vietnamese, even when source looks odd.
2. **Language validity (LLM/expert review).** Check simplified Chinese morphology, context-specific sense, classifier/measure words, polyphonic characters, Pinyin tone marks, spacing and grammatical naturalness. Optional libraries such as `pypinyin` can catch some transcription mistakes but cannot establish contextual meaning automatically.
3. **Typography (deterministic).** Real text nodes + Unicode NFC + bundled or installed multilingual fonts; content text reads back exactly. Verify overflow, minimum font size and screenshot legibility.
4. **Artwork alignment (visual review).** Does illustration actually correspond to the phrase? If it shows coffee while the phrase says fruit juice, reject that art tile; leave text untouched.

## Potential mistakes to flag

- Incorrect Pinyin or mixed tone-mark placement
- Incorrect tone sandhi or transcription of common combinations in conversational Pinyin
- Unsuitable translation (e.g. `烤玉米` is "ngô nướng/bắp nướng", not simply "corn")
- Terms ambiguous by situation or dialect
- User table that contains both 1-word entries and sentence-length entries with too little space
- Latin letters displayed as fake Hanzi or missing Vietnamese diacritics

Do not make strong claims of 100% accuracy without independent linguistic review. Never use OCR as the primary text correctness strategy for a code-composited poster.

## Sample correction log

```json
[{"item_id":"07", "field":"pinyin", "original":"...", "proposed":"...", "reason":"context-specific reading", "status":"needs-review"}]
```

If user provides exact text and requests preservation, report the concern separately instead of changing it in the published image without consent.
