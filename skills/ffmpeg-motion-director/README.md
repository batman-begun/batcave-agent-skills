# FFmpeg Motion Director v0.4.1

Turn still images into short cinematic clips with 15 procedural motion effects. The agent inspects the images and chooses an effect for each scene. The bundled Python and FFmpeg runner renders the motion plan locally, checks the video and packages the batch. The default clip is a silent 30-second, 854 × 480, 24 fps H.264 MP4.

[See a rendered clip and all 15 effects](../../docs/showcase/ffmpeg-motion-director/README.md).

## Use with an agent

Load [SKILL.md](SKILL.md) and explicitly ask to use `ffmpeg-motion-director` on your images. The agent needs access to the local input files, a shell, a way to inspect contact sheets and QC previews, and a way to deliver the ZIP files. After each batch, say **Next** to continue. The final batch can have fewer than five clips.

## Setup

Install Python 3.10 or newer and put `ffmpeg` (with `libx264`) and `ffprobe` on your PATH. From this skill directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r assets/requirements.txt
ffmpeg -hide_banner -encoders
ffprobe -version
```

Use the published Python packages or a compatible local environment. Dependency installation may require network access. Batch jobs run locally using the files and executables above.

## Use the CLI directly

```bash
python assets/batch.py prepare --input photo.jpg more-photos.zip --project ./motion-job
# Inspect contact_sheets/ and fill fx_override and visual_notes in motion_plan.csv.
python assets/batch.py render --project ./motion-job --batch 1
python assets/batch.py status --project ./motion-job
```

Use a fresh project path. `--input` accepts image files, directories and ZIPs in the requested order. The runner accepts up to 600 images, 100 MiB per accepted image and 2 GiB total uncompressed accepted image data. Render from archives you trust and allow space for staged images, clips and ZIPs.

Each batch ZIP contains the MP4s, plan, source metadata, report, checkpoint and QC preview. These files can include original input paths or filenames. Review them before sharing an output ZIP. Technical QC checks dimensions, duration, frame count, pixel format and decode. Review the preview for visual quality.

The public skill and bundled renderer source are [MIT licensed](LICENSE). Dependencies retain their own licenses.
