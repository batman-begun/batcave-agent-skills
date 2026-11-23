#!/usr/bin/env bash
# Downloads original Hallmark v2 from upstream and installs its complete skill without overwriting existing files.
set -euo pipefail
SOURCE_URL="https://github.com/Nutlope/hallmark.git"
COMMIT="04977e15f3dfd6ee4b74c887dac3eb52665d6c92"
SOURCE="${HALLMARK_SOURCE_DIR:-$HOME/src/hallmark-upstream}"
TARGET="${HALLMARK_SKILL_TARGET:-$HOME/.config/opencode/skills/hallmark}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "${1:-}" == "--help" ]]; then
  printf '%s\n' 'Usage: bash bootstrap-full-hallmark.sh [--help]' \
    'Optional: HALLMARK_SOURCE_DIR=/path/to/source HALLMARK_SKILL_TARGET=/path/to/target' \
    'Requires git + python3 + internet. Never overwrites the target.'
  exit 0
fi
if [[ $# -gt 0 ]]; then printf 'Unknown argument: %s\n' "$1" >&2; exit 2; fi
command -v git >/dev/null || { echo 'git required' >&2; exit 2; }
command -v python3 >/dev/null || { echo 'python3 required' >&2; exit 2; }
if [[ -e "$TARGET" ]]; then echo "Target exists; not overwriting: $TARGET" >&2; exit 2; fi
if [[ -e "$SOURCE" ]]; then
  if [[ ! -d "$SOURCE/.git" ]]; then echo "Source path exists but is not a git checkout: $SOURCE" >&2; exit 2; fi
  HAVE="$(git -C "$SOURCE" rev-parse HEAD)"
  if [[ "$HAVE" != "$COMMIT" ]]; then echo "Existing clone at $SOURCE is $HAVE, not pinned $COMMIT. Won't alter it." >&2; exit 2; fi
else
  mkdir -p "$(dirname "$SOURCE")"
  git clone --filter=blob:none "$SOURCE_URL" "$SOURCE"
  git -C "$SOURCE" checkout --detach "$COMMIT"
fi
python3 "$SCRIPT_DIR/verify-full-source.py" "$SOURCE/skills/hallmark"
mkdir -p "$(dirname "$TARGET")"
cp -R "$SOURCE/skills/hallmark" "$TARGET"
python3 "$SCRIPT_DIR/verify-full-source.py" "$TARGET"
echo "Installed complete upstream Hallmark at $TARGET (pinned $COMMIT)."
echo 'Node 18+ required for theme & SlopLint scripts; Chrome and puppeteer-core needed for browser checks.'
