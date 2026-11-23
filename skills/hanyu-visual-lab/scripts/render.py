#!/usr/bin/env python3
"""HanYu Visual Lab: deterministic tri-language typography + image composition.

This renderer does not contact any image API or LLM.  The calling agent prepares
lesson.json and optionally puts textless illustration images in assets/illustrations.
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html
import io
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

SCHEMA_VERSION = "1.0"
PALETTES = [
    ("#e3f0ff", "#6ca7e7", "#f2f8ff"),
    ("#e9f9dd", "#79c37e", "#f7fff3"),
    ("#f1e6ff", "#af89e8", "#fbf8ff"),
    ("#ffe5f0", "#ed91bb", "#fff6fb"),
    ("#fff1d5", "#e6b35b", "#fffbf1"),
]
CJK_RE = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")
VALID_FORMATS = {"vocabulary-clusters", "flow-grammar", "dialogue", "auto"}


def e(value):
    return html.escape(str(value), quote=True)


def normalize(value):
    return unicodedata.normalize("NFC", str(value).strip())


def validate(data: dict) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    if not isinstance(data, dict):
        return ["Root must be a JSON object"], warnings
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version must be 1.0")
    if data.get("source_mode") not in ("data", "topic"):
        errors.append("source_mode must be data or topic")
    if data.get("layout", "auto") not in VALID_FORMATS:
        errors.append("Unknown layout")
    if not normalize(data.get("title_zh", "")) or not normalize(data.get("subtitle_vi", "")):
        errors.append("title_zh and subtitle_vi are required")
    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        errors.append("sections must be nonempty array")
        return errors, warnings
    if len(sections) > 5:
        warnings.append("More than 5 sections likely crowds poster; split is recommended")
    ids = []
    total = 0
    for sidx, section in enumerate(sections):
        if not isinstance(section, dict):
            errors.append(f"Section {sidx+1} is not an object")
            continue
        if not normalize(section.get("title_vi", "")):
            errors.append(f"Section {sidx+1} has no title_vi")
        items = section.get("items")
        if not isinstance(items, list) or not items:
            errors.append(f"Section {sidx+1} has no items")
            continue
        if len(items) > 7:
            warnings.append(f"Section {sidx+1} contains {len(items)} items; likely small text")
        for ix, item in enumerate(items):
            total += 1
            if not isinstance(item, dict):
                errors.append(f"Item {sidx+1}.{ix+1} not an object")
                continue
            ident = normalize(item.get("id", ""))
            if not ident:
                errors.append(f"Item {sidx+1}.{ix+1} missing id")
            ids.append(ident)
            for key in ("hanzi", "pinyin", "vi"):
                if not normalize(item.get(key, "")):
                    errors.append(f"Item {ident or sidx+1} missing {key}")
            if not CJK_RE.search(normalize(item.get("hanzi", ""))):
                warnings.append(f"Item {ident}: Chinese expression contains no Chinese character")
            if re.search(r"[\u4e00-\u9fff]", normalize(item.get("pinyin", ""))):
                errors.append(f"Item {ident}: pinyin contains Hanzi")
            if len(normalize(item.get("vi", ""))) > 75:
                warnings.append(f"Item {ident}: very long Vietnamese meaning")
    if len(ids) != len(set(ids)):
        errors.append("Duplicate item ids")
    if total > 20:
        errors.append("More than 20 items: split into multiple lessons before rendering")
    if total < 4:
        warnings.append("Fewer than 4 items: poster may look sparse")
    mem = data.get("memory_item_ids", [])
    if not isinstance(mem, list):
        errors.append("memory_item_ids must be an array")
    elif len(mem) > 8:
        errors.append("memory_item_ids has more than 8 elements")
    elif len(set(mem)) != len(mem):
        errors.append("memory_item_ids contains duplicates")
    else:
        for mid in mem:
            if str(mid) not in ids:
                errors.append(f"Memory item id {mid} does not exist")
    return errors, warnings


def dict_from_json(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("title_zh", "subtitle_vi", "topic"):
        if key in data:
            data[key] = normalize(data[key])
    for s in data.get("sections", []):
        s["title_vi"] = normalize(s["title_vi"])
        for item in s["items"]:
            for key in ("id", "hanzi", "pinyin", "vi"):
                item[key] = normalize(item[key])
    return data


def load_table(path: Path) -> list[dict]:
    """Import strict 3-column TSV, CSV, or pipe table. For whitespace input,
    agent must first perform structured extraction (pinyin/Vietnamese boundary ambiguous).
    """
    content = path.read_text(encoding="utf-8-sig").strip()
    if not content:
        raise ValueError("Table is empty")
    if path.suffix.lower() == ".json":
        value = json.loads(content)
        if not isinstance(value, list):
            raise ValueError("JSON table must be an array of objects")
        rows = value
    else:
        sample = content.splitlines()[0]
        delim = "\t" if "\t" in sample else ("|" if "|" in sample else ",")
        rows = []
        for line in csv.reader(io.StringIO(content), delimiter=delim):
            if not line or all(not x.strip() for x in line):
                continue
            if len(line) == 4 and line[0].strip().isdigit():
                line = line[1:]
            if len(line) != 3:
                raise ValueError(f"Expected 3 columns, got {len(line)}: {line!r}")
            if line[0].strip().lower() in {"hanzi", "chinese", "中文", "cụm từ"}:
                continue
            rows.append(dict(zip(("hanzi", "pinyin", "vi"), map(normalize, line))))
    result = []
    for ix, row in enumerate(rows, start=1):
        if not isinstance(row, dict) or not all(row.get(c) for c in ("hanzi", "pinyin", "vi")):
            raise ValueError(f"Invalid three-column row {ix}")
        result.append({"id": f"{ix:02}", **{k: normalize(row[k]) for k in ("hanzi", "pinyin", "vi")}})
    return result


def item_index(data):
    return {x["id"]: x for s in data["sections"] for x in s["items"]}


def data_uri(path):
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg" if path.suffix.lower() in (".jpg", ".jpeg") else "image/webp"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def fallback_art(ident, color):
    # This is deliberately a fallback pictogram, not a claim of AI-generated illustration.
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="380" height="130" viewBox="0 0 380 130">
    <ellipse cx="190" cy="120" rx="163" ry="9" fill="{color}" opacity=".25"/>
    <circle cx="188" cy="66" r="53" fill="{color}" opacity=".18"/>
    <path d="M166 61c-3-15 12-24 24-13 12-11 27-2 24 13-2 12-24 27-24 27s-22-15-24-27z" fill="{color}" opacity=".84"/>
    <g fill="#ffcc63"><path d="M84 50l5 16 16 5-16 5-5 16-5-16-16-5 16-5z"/>
    <path d="M298 26l4 12 12 4-12 4-4 12-4-12-12-4 12-4z"/></g>
    </svg>'''
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def make_html(data, root: Path, target=1600):
    idx = item_index(data)
    count = sum(len(s["items"]) for s in data["sections"])
    memory = data.get("memory_item_ids", []) or list(idx)[:min(7, len(idx))]
    colors = PALETTES
    sections_markup = []
    if len(data["sections"]) <= 2:
        ratio = "low"
    elif len(data["sections"]) >= 5:
        ratio = "high"
    else:
        ratio = "normal"
    for sec_no, section in enumerate(data["sections"], start=1):
        base, edge, light = colors[(sec_no-1) % len(colors)]
        cards = []
        for item in section["items"]:
            ident = item["id"]
            apath = None
            for ext in ("png", "jpg", "jpeg", "webp"):
                candidate = root / "assets" / "illustrations" / f"{ident}.{ext}"
                if candidate.exists():
                    apath = candidate
                    break
            image_uri = data_uri(apath) if apath else fallback_art(ident, edge)
            cards.append(f'''<article class="entry-card" data-entry="{e(ident)}" style="--panel-bg:{light};--panel-border:{edge}">
               <div class="hanzi text-check" data-type="hanzi" lang="zh-Hans">{e(item['hanzi'])}</div>
               <div class="pinyin text-check" data-type="pinyin">{e(item['pinyin'])}</div>
               <div class="vi text-check" data-type="vi">→ {e(item['vi'])}</div>
               <div class="illustration"><img alt="" src="{image_uri}"/></div>
               </article>''')
        columns = len(section["items"])
        sections_markup.append(f'''<section class="lesson-section" style="--section-bg:{base};--section-edge:{edge};--section-cols:{columns}">
        <div class="section-label">{sec_no}. {e(section['title_vi'])}</div>
        <div class="cards-row">{''.join(cards)}</div>
        </section>''')
    mem_cards=[]
    for mid in memory:
        item=idx[mid]
        mem_cards.append(f'''<div class="memory-card" data-memory="{e(mid)}"><div class="mem-zh text-check" lang="zh-Hans">{e(item['hanzi'])}</div><div class="mem-py text-check">{e(item['pinyin'])}</div><div class="mem-vi text-check">{e(item['vi'])}</div></div>''')
    footer_cols=len(mem_cards)
    poster_title=e(data['title_zh'])
    poster_sub=e(data['subtitle_vi'])
    # HTML also serves as the editable, viewable source. All image sources are embedded.
    css=r'''*{box-sizing:border-box}html,body{margin:0;padding:0;overflow:hidden;background:#fff}
    body{font-family:'Noto Sans', 'Arial',sans-serif;color:#322521}
    .poster{position:relative;width:1600px;height:1200px;overflow:hidden;background:linear-gradient(115deg,#fffefb,#fff5f7 45%,#fffefb);padding:14px 22px 18px;display:grid;grid-template-rows:125px minmax(0,1fr) 154px;gap:9px}
    .poster:before{content:'✦  ♡  ✦  ♡  ✦';position:absolute;top:5px;left:29px;font-size:20px;letter-spacing:10px;color:#e5a2c9;z-index:0}
    .header{position:relative;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:6px;padding:4px 20px}
    .wood-banner{border:5px solid #9f6745;border-radius:27px;background:linear-gradient(#f5d9a4,#f3bb79 53%,#f6dbb2);box-shadow:0 5px 0 #e3b37c,0 8px 0 #fff4e2;min-width:68%;padding:5px 28px;text-align:center;z-index:1}
    .title{font-family:'Noto Sans CJK SC','Noto Sans',sans-serif;font-size:40px;line-height:1.22;font-weight:900;white-space:nowrap}
    .subtitle{background:linear-gradient(90deg,#ffc6df,#ffa7cf,#ffcade);padding:3px 30px;border-radius:40px;border:3px solid #fff;color:#563348;box-shadow:0 0 0 2px #e98eb5;font-weight:800;font-size:21px;white-space:nowrap;z-index:1}
    .header-deco{position:absolute;font-size:68px;top:9px;z-index:0;opacity:.85}.header-deco.left{left:42px}.header-deco.right{right:42px}
    .main{min-height:0;display:grid;grid-template-rows:repeat(var(--section-count),minmax(0,1fr));gap:9px}
    .lesson-section{display:flex;flex-direction:column;min-height:0;border:3px solid var(--section-edge);background:var(--section-bg);border-radius:24px;padding:5px 9px 9px}
    .section-label{font-weight:900;font-size:25px;height:32px;line-height:30px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:0 14px}
    .cards-row{flex:1;display:grid;grid-template-columns:repeat(var(--section-cols),minmax(0,1fr));gap:7px;min-height:0}
    .entry-card{background:var(--panel-bg);border:2px solid var(--panel-border);border-radius:21px;position:relative;overflow:hidden;min-width:0;min-height:0;padding:9px 10px 3px;display:flex;flex-direction:column}
    .hanzi{font-family:'Noto Sans CJK SC', 'Noto Sans CJK',sans-serif;font-weight:900;font-size:30px;line-height:1.25;overflow-wrap:anywhere;max-height:75px}
    .pinyin{font-weight:600;font-size:16px;line-height:1.3;overflow-wrap:break-word;margin-top:3px}
    .vi{font-size:17px;font-weight:650;line-height:1.23;overflow-wrap:break-word;margin-top:3px}
    .illustration{flex:1;min-height:28px;max-height:108px;margin-top:1px;display:flex;justify-content:center;align-items:center;overflow:hidden}
    .illustration img{height:100%;width:100%;object-fit:contain}
    .footer{border:3px solid #e9b263;border-radius:23px;background:linear-gradient(#fff5ce,#fff7e6);padding:3px 11px 10px;display:flex;flex-direction:column;min-height:0}
    .footer-label{height:30px;line-height:29px;font-size:23px;font-weight:900}
    .memory-row{display:grid;grid-template-columns:repeat(var(--memory-cols),minmax(0,1fr));gap:6px;flex:1;min-height:0}
    .memory-card{background:#fffaf0;border:2px solid #f0c47d;border-radius:16px;min-width:0;padding:8px 8px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;text-align:center;overflow:hidden}
    .mem-zh{font-family:'Noto Sans CJK SC',sans-serif;font-weight:900;font-size:21px;line-height:1.2;overflow-wrap:anywhere}
    .mem-py{font-size:14px;font-weight:600;line-height:1.2;overflow-wrap:break-word}
    .mem-vi{font-size:14px;line-height:1.15;overflow-wrap:break-word}
    .bottom-garden{position:absolute;bottom:0px;right:0;left:0;pointer-events:none;font-size:24px;color:#8bc99d;text-align:center;opacity:.16;letter-spacing:18px;}
    '''
    nsec=len(data["sections"])
    poster=f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"/><meta name="viewport" content="width=1600, initial-scale=1"><style>{css}</style></head>
    <body><div class="poster" style="--section-count:{nsec};--memory-cols:{footer_cols}">
    <header class="header"><div class="header-deco left">✿ ♫</div><div class="wood-banner"><div class="title" lang="zh-Hans">{poster_title} · 超实用词汇</div></div>
    <div class="subtitle">{poster_sub}</div><div class="header-deco right">✦ ♡</div></header>
    <main class="main">{''.join(sections_markup)}</main>
    <footer class="footer"><div class="footer-label">★ Thanh ghi nhớ</div><div class="memory-row">{''.join(mem_cards)}</div></footer>
    <div class="bottom-garden">✿ ♡ ✿ ♡ ✿ ♡ ✿ ♡ ✿</div></div></body></html>'''
    return poster


FITTING_JS = r'''async () => {
 await document.fonts.ready;
 const issues=[];
 const resize=(el,min)=>{
   let style=getComputedStyle(el); let current=parseFloat(style.fontSize); let guard=0;
   while((el.scrollHeight>el.clientHeight+2 || el.scrollWidth>el.clientWidth+2) && current>min && guard++<40){
     current=Math.max(min,current-1);el.style.fontSize=current+'px';
   }
   if(el.scrollHeight>el.clientHeight+3 || el.scrollWidth>el.clientWidth+3){
       issues.push({type:'text-overflow',entry:el.closest('[data-entry]')?.dataset.entry||el.closest('[data-memory]')?.dataset.memory||'header',text:el.textContent.slice(0,80)});
   }
 };
 for(const el of document.querySelectorAll('.text-check')){let klass=el.className;
   resize(el, klass.includes('hanzi')?19:klass.includes('pinyin')?12:klass.includes('mem-zh')?15:11);
 }
 for(const el of document.querySelectorAll('.section-label,.title,.subtitle'))resize(el,el.classList.contains('title')?24:16);
 for(const card of document.querySelectorAll('.entry-card')){
   const x=card.querySelector('.hanzi'),y=card.querySelector('.pinyin'),z=card.querySelector('.vi'),art=card.querySelector('.illustration');
   const r=(p)=>p.getBoundingClientRect();
   if(r(z).bottom>r(art).top+2)issues.push({type:'text-art-overlap',entry:card.dataset.entry});
   if(r(art).height<24)issues.push({type:'art-zone-too-small',entry:card.dataset.entry});
 }
 for(const el of document.querySelectorAll('.lesson-section,.footer,.poster'))if(el.scrollHeight>el.clientHeight+3)issues.push({type:'block-overflow',block:el.className});
 return {issues,dimensions:{width:document.querySelector('.poster').offsetWidth,height:document.querySelector('.poster').offsetHeight},fontReady:document.fonts.status,elementCount:document.querySelectorAll('[data-entry]').length,renderedText:Array.from(document.querySelectorAll('[data-entry]')).map(el=>({id:el.dataset.entry,hanzi:el.querySelector('.hanzi').textContent,pinyin:el.querySelector('.pinyin').textContent,vi:el.querySelector('.vi').textContent.replace(/^→\s*/, '')}))};
}'''


def build(lesson_path:Path, out_dir:Path, art_root:Path|None=None, png=True):
    data=dict_from_json(lesson_path)
    errors,warnings=validate(data)
    if errors:
        raise ValueError("Dataset validation failed:\n"+"\n".join("- "+x for x in errors))
    out_dir.mkdir(parents=True,exist_ok=True)
    root=art_root or lesson_path.parent
    doc=make_html(data,root)
    (out_dir/"infographic.html").write_text(doc,encoding="utf-8")
    expected={i['id']:(i['hanzi'],i['pinyin'],i['vi']) for s in data['sections'] for i in s['items']}
    art_ids=[]
    missing_art=[]
    for ident in expected:
        paths=[root/'assets'/'illustrations'/f'{ident}.{ext}' for ext in ('png','jpg','jpeg','webp')]
        (art_ids if any(path.exists() and path.stat().st_size>100 for path in paths) else missing_art).append(ident)
    qa={"status":"not-rendered", "warnings":warnings,"issues":[],"source_mode":data['source_mode'],"item_count":len(expected),"input_sha256":hashlib.sha256(lesson_path.read_bytes()).hexdigest(),"illustrations":{"present":len(art_ids),"total":len(expected),"missing_ids":missing_art}}
    if missing_art:
        qa['warnings'].append(f'{len(missing_art)} illustration(s) missing: result is a layout preview, not completed kawaii art')
    if png:
        if sync_playwright is None:
            raise RuntimeError("Playwright Python not installed. Run: pip install playwright; then install Chromium if needed")
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True,executable_path="/usr/bin/chromium" if Path('/usr/bin/chromium').exists() else None,args=['--no-sandbox'])
            page=browser.new_page(viewport={"width":1600,"height":1200},device_scale_factor=2)
            page.set_content(doc,wait_until="load")
            result=page.evaluate(FITTING_JS)
            qa.update(result)
            actual={it['id']:(it['hanzi'],it['pinyin'],it['vi']) for it in result['renderedText']}
            if actual!=expected:
                qa['issues'].append({"type":"source-text-mismatch", "details":"Rendered text differs from lesson JSON"})
            if result['fontReady']!='loaded':
                qa['issues'].append({"type":"fonts-not-loaded"})
            for itm in page.evaluate("Array.from(document.querySelectorAll('.entry-card img')).map(x=>({id:x.closest('[data-entry]').dataset.entry,ok:x.complete && x.naturalWidth>0}))"):
                if not itm['ok']:
                    qa['issues'].append({'type':'broken-illustration', 'entry':itm['id']})
            qa['status']=('FAIL' if qa['issues'] else 'PASS_ILLUSTRATED' if not missing_art else 'PASS_LAYOUT_PREVIEW')
            page.screenshot(path=str(out_dir/'infographic.png'),full_page=False)
            browser.close()
    else:
        qa['status']='HTML-ONLY'
    (out_dir/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa


def cmd_import(args):
    items=load_table(Path(args.input))
    # This is a staging file, not a finished lesson plan. The agent must infer
    # the umbrella topic and section groupings before calling render.
    Path(args.output).write_text(json.dumps({"schema_version":"1.0","source_mode":"data","items":items,"instruction":"Agent: infer topic/sections and emit complete lesson.json without rewriting item text."},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f"Staged {len(items)} rows: {args.output}")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    imp=sub.add_parser('import',help='Import strict 3-column TSV, CSV, pipe table, or JSON array')
    imp.add_argument('input');imp.add_argument('--output',default='staging.json');imp.set_defaults(func=cmd_import)
    check=sub.add_parser('validate',help='Validate full lesson.json')
    check.add_argument('lesson')
    render=sub.add_parser('render',help='Render full lesson JSON into HTML and PNG')
    render.add_argument('lesson');render.add_argument('--out',default='output');render.add_argument('--art-root',default=None);render.add_argument('--html-only',action='store_true')
    args=parser.parse_args()
    if args.command=='validate':
        data=dict_from_json(Path(args.lesson));errors,warnings=validate(data)
        print(json.dumps({"status":"PASS" if not errors else "FAIL","errors":errors,"warnings":warnings},ensure_ascii=False,indent=2))
        if errors:sys.exit(2)
    elif args.command=='render':
        try:qa=build(Path(args.lesson),Path(args.out),Path(args.art_root) if args.art_root else None,png=not args.html_only)
        except Exception as exc:print(str(exc),file=sys.stderr);sys.exit(2)
        print(json.dumps(qa,ensure_ascii=False,indent=2)[:10000])
        if qa['status']=='FAIL':sys.exit(3)
    else:args.func(args)

if __name__=='__main__':main()
