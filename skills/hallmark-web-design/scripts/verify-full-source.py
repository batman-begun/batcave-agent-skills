#!/usr/bin/env python3
"""Check structural parity of a full locally-cloned Hallmark skill at a pinned commit.
This is not a unit-test runner, browser test, or security audit.
"""
import json, sys
from pathlib import Path

def validate(root):
    root=Path(root)
    themes=root/'references'/'themes'
    idx=themes/'index.json'
    failures=[]
    if not idx.is_file(): failures.append('missing references/themes/index.json')
    data={}
    if idx.is_file():
        try: data=json.loads(idx.read_text(encoding='utf-8'))
        except (ValueError,UnicodeDecodeError) as e: failures.append('invalid index.json: '+str(e))
    items=data.get('themes',[]) if isinstance(data,dict) else []
    if len(items)!=50: failures.append(f'index themes = {len(items)}, expected 50')
    slugs={t.get('slug') for t in items if isinstance(t,dict)}
    if len(slugs)!=50: failures.append(f'unique slugs = {len(slugs)}, expected 50')
    md={x.stem for x in themes.glob('*.md') if x.name!='README.md'}
    jpg={x.stem for x in themes.glob('*.jpg')}
    if len(md)!=50: failures.append(f'theme md = {len(md)}, expected 50')
    if len(jpg)!=50: failures.append(f'theme jpg = {len(jpg)}, expected 50')
    if md!=slugs: failures.append(f'missing/extra theme markdown: {sorted(slugs-md)} / {sorted(md-slugs)}')
    if jpg!=slugs: failures.append(f'missing/extra preview jpg: {sorted(slugs-jpg)} / {sorted(jpg-slugs)}')
    essential=['SKILL.md','LICENSE','agents/openai.yaml',
      'references/gates.md','references/flow.md','references/redesign.md',
      'scripts/theme.mjs','scripts/sloplint.mjs','scripts/sloplint-render.mjs',
      'scripts/refcheck.mjs','scripts/photos.json']
    for name in essential:
        if not (root/name).is_file(): failures.append('missing '+name)
    blob_count=sum(1 for p in root.rglob('*') if p.is_file())
    total_bytes=sum(p.stat().st_size for p in root.rglob('*') if p.is_file())
    # Manifest describes a frozen upstream. Exact counts are a useful extra check.
    if blob_count!=187: failures.append(f'files = {blob_count}, expected 187')
    if total_bytes!=7079805: failures.append(f'bytes = {total_bytes}, expected 7079805')
    result={'pass':not failures,'path':str(root),'files':blob_count,'bytes':total_bytes,
      'themes_markdown':len(md),'theme_previews':len(jpg),'failures':failures}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if not failures else 1

if __name__=='__main__':
    if len(sys.argv)!=2: print('usage: python3 verify-full-source.py PATH',file=sys.stderr);sys.exit(2)
    sys.exit(validate(sys.argv[1]))
