#!/usr/bin/env python3
"""Generate or verify registry catalog from skill frontmatter and optional metadata."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from registry_core import RegistryError, build

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='fail if generated catalog differs from committed catalog')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        generated = json.dumps(build(args.root), ensure_ascii=False, indent=2) + '\n'
        target = args.root / 'catalog.json'
        if args.check:
            current = target.read_text(encoding='utf-8') if target.exists() else ''
            if current != generated:
                print('FAIL: catalog.json is missing or stale. Run python3 scripts/build_catalog.py', file=sys.stderr)
                return 1
            print('PASS: catalog.json matches source skill metadata')
        else:
            target.write_text(generated, encoding='utf-8')
            print(f'Wrote {target}')
        return 0
    except (RegistryError, OSError, ValueError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
