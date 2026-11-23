# Canonical lesson JSON — HanYu Visual Lab v1

Required keys:

```json
{
  "schema_version": "1.0",
  "source_mode": "data",
  "layout": "vocabulary-clusters",
  "topic": "Ở nhà thư giãn",
  "title_zh": "在家休闲",
  "subtitle_vi": "Ở nhà thư giãn – Học tiếng Trung thật vui!",
  "sections": [
    {
      "title_vi": "Nghe nhạc & ca hát",
      "items": [
        {
          "id": "01",
          "hanzi": "听音乐",
          "pinyin": "tīng yīnyuè",
          "vi": "nghe nhạc",
          "art_brief": "Cheerful chibi girl listening through pastel pink headphones"
        }
      ]
    }
  ],
  "memory_item_ids": ["01"],
  "corrections": [],
  "uncertain_items": []
}
```

- `source_mode`: `data` for user-supplied entries; `topic` for model-authored table.
- `layout`: `vocabulary-clusters`, `flow-grammar`, `dialogue`, or `auto`. v1 compositor uses a shared section-card layout for all three; specialized layout variants are **future extensions**, not already implemented.
- `topic`: pedagogical concept, optional but recommended.
- `title_zh`, `subtitle_vi`: required, compact, textual (not image-model lettering).
- `sections`: 1–5 sections, each with `title_vi` and `items`.
- `items`: unique `id`, `hanzi`, `pinyin`, `vi`, optional `art_brief`.
- `memory_item_ids`: optional list of at most 8 IDs, every ID must reference an existing item.
- `corrections`: when reviewing user-supplied material, report `item_id`, `field`, `original`, `proposed`, `reason`, `status`.
- `uncertain_items`: things requiring source confirmation or expert review.

## Mode A: Data preservation

Conserve the **multiset of input triplets** and their exact normalized Unicode content (except documented corrections). Section grouping and order are allowed; do not accidentally drop an item because of repeated Hanzi in different contexts. `memory_item_ids` only duplicates for pedagogy, not an extra source row.

## Mode B: Topic authoring

An LLM writes a complete list itself. Good selection:
- 8–16 short, everyday, connected Chinese phrases
- Accurate Pinyin with tone marks (not raw machine transliteration blindly)
- Short, natural Vietnamese meanings
- One real scenario or natural progression
- Avoid overrepresenting synonyms, overly abstract words, taboo/sensitive assumptions or fake idioms

Example subject `hôn nhân & gia đình` should usually focus on one scenario such as introducing family members, discussing relationships or celebrating a wedding; don't mix all of these into a single poster unless the user asks for a broad vocabulary list.

## Exact text integrity

The compositor copies only `hanzi`, `pinyin`, and `vi` from the JSON to real text nodes; HTML entity escaping prevents injected tags. The QA script reads text nodes back and compares them with input, so a mismatched string is a hard failure. This does not establish whether a supplied translation is correct.
