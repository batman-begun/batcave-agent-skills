# Upstream parity and provenance (21 Nov 2026)

Repository: https://github.com/Nutlope/hallmark
Pinned commit: `04977e15f3dfd6ee4b74c887dac3eb52665d6c92` (GitHub commit timestamp 2026-11-11 11:56:04 UTC)
License: MIT; original `skills/hallmark/LICENSE` retained by a full local clone.

Verified GitHub tree inventory: **187 file blobs within `skills/hallmark/`, 7,079,805 bytes**; **50 theme `.md`**, **50 matched `.jpg`** (plus theme `README.md` and `index.json`). Original payload includes `skills/hallmark/SKILL.md`, `agents/openai.yaml`, reference documents and macrostructures, and `scripts/theme.mjs`, `scripts/sloplint.mjs`, `scripts/sloplint-render.mjs`, `scripts/refcheck.mjs`, tests, and `scripts/photos.json` (photo index only, not photograph binaries).

**Hallmark Web Design package status:** This adapter has a complete 50-item theme *index*, these operating instructions and a pinned-source local bootstrap script. It does **NOT** embed the actual 187-file upstream payload, the original theme definitions, the 50 image binaries, the photo data or runnable browser QA. It accesses all textual original files through GitHub or a verified local checkout and offers a local install to recover the full 187-file payload for OpenCode/T3.

## Actual parity checks after local bootstrap

Use `python3 scripts/verify-full-source.py <path-to-cloned-skill>` from this adapter's directory; pass should confirm 50 `.md`, 50 `.jpg`, theme index, no missing themes, required scripts and per-file presence. If the source clone is not accessible, mark runtime parity **unverified**, never passed.

Original source file URLs are at `https://github.com/Nutlope/hallmark/tree/04977e15f3dfd6ee4b74c887dac3eb52665d6c92/skills/hallmark`. To upgrade the pin, verify upstream changes and run checks against a real cloned checkout first; do not point blindly at moving `main`.
