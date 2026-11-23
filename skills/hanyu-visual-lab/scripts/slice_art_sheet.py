#!/usr/bin/env python3
"""Crop a textless image-generation sprite sheet into item illustrations.

Each cell must have equal dimensions; ordering is left-to-right, then top-to-bottom.
This tool does not infer which visual belongs to which word. A human/agent must
review scene-to-item mapping before publish.
"""
import argparse
from pathlib import Path
from PIL import Image


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('sheet',help='Input PNG/JPEG/WebP textless illustration sheet')
    p.add_argument('--rows',type=int,required=True)
    p.add_argument('--cols',type=int,required=True)
    p.add_argument('--ids',required=True,help='Comma separated ordered item IDs, e.g. 01,02,03,04')
    p.add_argument('--out',default='assets/illustrations')
    args=p.parse_args()
    ids=[x.strip() for x in args.ids.split(',') if x.strip()]
    if args.rows<1 or args.cols<1 or len(ids)!=args.rows*args.cols:
        p.error('rows*cols must equal the number of IDs (use separate sheets for leftovers)')
    if len(set(ids))!=len(ids):p.error('Duplicate IDs')
    output=Path(args.out);output.mkdir(parents=True,exist_ok=True)
    with Image.open(args.sheet) as im:
        im=im.convert('RGBA')
        w,h=im.size
        if w%args.cols or h%args.rows:
            p.error(f'Sheet dimensions {w}x{h} must be divisible by {args.cols}x{args.rows}')
        cw,ch=w//args.cols,h//args.rows
        if cw<220 or ch<150:
            print(f'WARNING: small illustration cells {cw}x{ch}; chibi details may be lost')
        for i,ident in enumerate(ids):
            col,row=i%args.cols,i//args.cols
            crop=im.crop((col*cw,row*ch,(col+1)*cw,(row+1)*ch))
            crop.save(output/f'{ident}.png')
        print(f'Wrote {len(ids)} PNG crops, {cw}x{ch} per tile, to {output}')
        print('ACTION REQUIRED: visually verify each cropped scene matches the corresponding item ID.')

if __name__=='__main__':main()
