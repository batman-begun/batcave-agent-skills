---
name: ffmpeg-motion-director
description: "Use on explicit request to turn still images, folders or image ZIPs into cinematic 30-second videos. Inspect images, choose among 15 FFmpeg motion effects and deliver verified ZIPs of up to five clips per batch."
---

# FFmpeg Motion Director v0.4.1

## Invocation and intake (critical)

- **Explicit invocation only.** Start a render job when the user names this skill or explicitly requests this workflow. A plugin mention can serve as invocation where the host supports it. Descriptions and questions about the skill are informational.
- Accept **one image**, **multiple images**, any mixture of standalone files, folders and **ZIPs containing images**, or an image directory when available in the work environment. Images must be accessible as local files in the active Python workspace before starting. No storyboard or extra project context is required. If invoked without images, ask for images; do not fabricate them.
- **In-chat progress**: as soon as assets are accessible, read actual image count, report the count and calculated batch sizes, then visually inspect all contact sheets and any detailed images necessary. Present an intelligible structured summary in the conversation with an image count, batch 1/total status, per-image FX assignments and one short reason per image, plus completed/downloading status. Use native cards/tables when supported by the host; otherwise use a clear Markdown table. Do NOT claim a standalone graphical plugin app exists: this is a skills-only, in-chat orchestration interface.
- **No manual effect selection required**: the assistant acts as Motion Director, assigning visually appropriate FX for each image, documenting an evidence-based `visual_notes`. Do not blindly rotate presets or infer visual content from filenames only. Plan choices are auditable and user may override.

## Output and batch guarantee

- Every provided image yields **exactly one video**; never duplicate, drop, or pad images to fill a batch. Images are naturally ordered within each ZIP; standalone files are taken in input order.
- Partition into **consecutive batches of at most five videos**. For `N` images, use `ceil(N/5)` batches. The final batch has `N % 5` outputs when nonzero: examples `1→[1]`, `4→[4]`, `5→[5]`, `7→[5,2]`, `11→[5,5,1]`. This replaces v0.3's erroneous `5*N` ZIP count restriction.
- Unless user explicitly changes specs, **each video is 30 seconds, 854×480 (480p), 24fps, silent H.264/yuv420p MP4** (720 frames). No black borders, no generic fade to black; preserve image aspect by fill/crop with visual review.
- **Always create and verify one downloadable ZIP per rendered batch**, even if a batch has just one MP4. ZIP contains only that batch's MP4(s), `motion_plan.csv`, `source.json`, `render_report.csv`, `checkpoint.json`, and `qc_preview.jpg`. Show link to ZIP prominently; optional individual clips can be linked too. Never provide bare MP4s without the batch ZIP.
- **Stop after each batch**. Proceed to the next batch only when user says Next/continue (or equivalent explicit authorization), even if the project has more images. Do not silently render remaining batches. A job of up to five images completes in batch 1.

## Actual executable pipeline

Run the bundled Python scripts in the active workspace. See [setup](README.md#setup) for Python, FFmpeg, FFprobe and image dependencies. Run the examples from the skill directory and set `--project` to a fresh path writable by the current runtime. The renderer consumes local files. Verify the output files before reporting completion.

### 1 — Prepare (any input count ≥1)

```bash
python assets/batch.py prepare --input image1.jpg image2.png --project ./motion-job
python assets/batch.py prepare --zip photos.zip --project ./motion-job
python assets/batch.py prepare --zip photos.zip --input extra.jpg --project ./motion-job
```

Use a fresh unique project directory. The runner validates image bytes, archive CRC, and source count, assigns `S001...`, preserves original filenames in `motion_plan.csv`, creates `source.json` and contact sheets. Only pass `--expect N` if the user explicitly specified a required count. Use `--input` to list multiple ZIPs or to preserve a specific order across mixed inputs. If combined with the single `--zip` shortcut, the shortcut ZIP is processed first. The runner accepts up to 600 images per job, with input size limits described in the [README](README.md).

### 2 — Intelligent visual direction

Inspect **all** generated `contact_sheets/*.jpg` and view individual source images in high resolution if faces, shadows or text are ambiguous. For each scene, fill the existing `fx_override` and `visual_notes` columns in `motion_plan.csv`; use *one of the 15 active FX* below (only `golden_hour` is an explicitly reported v0.3 legacy alias, never select it for new jobs). Keep visual intent, camera movement, face/text preservation, neighboring scenes' differences, and 30s temporal development in mind.

**Present the in-chat intelligent plan UI** after inspection: actual count, batch plan, each source's label, selected FX, why it suits the image, and which batch is being rendered. It is a truthful readout of asset inspection and `motion_plan.csv`, not a decorative UI claiming unsupported features.

### 3 — Render one authorized batch, full QC and ZIP

```bash
python assets/batch.py render --project ./motion-job --batch 1
# Later, ONLY on user Next:
python assets/batch.py render --project ./motion-job --batch 2
python assets/batch.py status --project ./motion-job
```

The batch runner invokes the renderer separately for each selected image and FX, asserts 720 frames/30 seconds/854×480/H.264/yuv420p, **decodes every frame with FFmpeg**, samples QC frames, writes a hash-aware checkpoint and render report, builds the batch ZIP, and checks ZIP CRC and expected number of MP4s. Check `qc_preview.jpg` **visually** for clipping, damaged faces, weak or duplicated motions; full decode only proves technical validity. If a clip is artistically unacceptable, update `motion_plan.csv` and force just the affected render when feasible; `--force` explicitly allows replacement. Do not hide missing files, skipped images, fallback effects, or errors. **No automatic whole-screen zoom fallback** if a premium FX fails; retry/choose a visually appropriate valid FX and report the change.

If execution context resets, recover files/checkpoint from available workspace or ask user for source assets and the last ZIP; never assert ephemeral renders survived.

## Final 15 first-class FX — art direction LOCKED by user

| FX | User-approved motion grammar | Camera | Constraint |
| --- | --- | --- | --- |
| `radial_refraction` | Concentric circular ripple bends underlying image pixels, cinematic amplitude | Locked | **Pure refraction**; NO glowing-circle overlay |
| `water_mirage` | Organic localized flowing liquid refraction bands, no uniform rubber-sheet wobble | Locked | Preserve important faces/text |
| `prism_glass` | Moving angular glass panes with real local image displacement and color splitting | Locked | Not just transparent polygon overlay |
| `cyber_glitch` | Short strong RGB channel tearing, offset blocks and scanline artifacts | Locked | Episodic, not permanent glitch |
| `tile_mosaic` | 11×6 / 66 independent tiles split, sway/rotate and reunite | Locked | Original image remains recognizable; matches approved 6s prototype |
| `shadow_reveal` | Pronounced diagonal shadow slats, **approximately 60°** with independent drifts | Locked | Contrast and edge softness varied, no image pan |
| `rhythmic_zoom` | Smooth centered cycles 1.00×↔1.17× (3-second period) | Deliberate zoom | No lateral drift, color flashes, or unexpected camera shake |
| `rain_glass` | Distinct rain streaks + individual drops on lens with local refraction | Locked | Not just lines scrolling vertically |
| `snow_dust` | Small sixfold symmetrical snowflakes, multiple depths, independent wind | Locked | Small, not giant flakes |
| `petals` | Recognizable notched sakura petals that tumble and follow individual trajectories | Locked | Use only when atmosphere suits image |
| `firestorm` | Individual ascending glowing embers and hot air atmosphere | Locked | Preserve critical details |
| `bokeh` | Smaller **hexagonal**, slightly blue-shifted aperture lights moving directionally | Locked | Avoid giant graphic circles |
| `sunbeam` | High-contrast angled light shafts, clearer **not larger** dust, irregular trajectories | Locked | Respect plausible light source |
| `film_burn` | Moving orange/red film-edge burns, glow, scratches and cinematic wear | Locked | Visibly differentiated from sunbeam |
| `cinematic_impact` | Localized shock-zoom/camera jolt on key beats | Intentional jolt | Do not become endless panning |

**Removed from active list:** `zoom_in`, `zoom_out`, `pan_left`, `pan_right`, `dream_pulse`, `flash`, `dream_memory`, `ripple`, `fog_rays`, `lens_flare`, `noir_focus`, `iris_reveal`. v0.3 `golden_hour` remains a deprecated alias for `sunbeam` only. Older plans referencing retired FX must be consciously migrated before rendering; **never silently reinterpret them as a visually unrelated effect**. Preserve already completed video clips and past plan records unless user requests rerender.

## Visual/director QC rules

- Use the same 15 approved motion signatures in all jobs; user may request scene-specific tweaks, but do not silently alter approved defaults.
- No generic pan across the whole photo (except the explicitly approved `rhythmic_zoom` and `cinematic_impact` behaviors).
- One 30s clip requires meaningful temporal continuity; avoid 5s FX followed by 25s near-stillness unless that rhythm is artistically intentional.
- Prefer independent particle motion (rain, snow, sakura, embers, bokeh, dust); avoid scrolling one pre-rendered particle sheet.
- Do not misrepresent these as true physically simulated 3D. Current engine uses image-space compositing, geometric masks, independent 2D particle paths, OpenCV frame synthesis and FFmpeg encode/decode.
- Keep original source order reproducible and `motion_plan.csv` auditable; report actual FX per exported clip, not just planned FX.
- When reporting an error, distinguish missing image files, missing runtime dependencies, FFmpeg rendering failure, visual QC failure, and ZIP packaging errors.

## Version migration and compatibility

v0.3 required ZIPs of `5*N` images. v0.4 accepts arbitrary `N>=1`, direct images and mixed ZIPs; partial final batches are first-class. v0.3 standalone camera effects were retired from the active menu. Defaults remain 480p, 30s, 24fps, five clips at most per batch, visual scene-specific direction and full-decode QC. Never claim standalone server rendering, always render in current available runtime.
