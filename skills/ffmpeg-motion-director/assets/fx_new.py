"""User-approved new effects: 66 independent tiles and centered rhythmic zoom."""
from __future__ import annotations
import cv2, numpy as np, math, random
W,H=854,480
COLS,ROWS=11,6
_rng=random.Random(11062026)
TILES=[]
for row in range(ROWS):
    y0=round(row*H/ROWS); y1=round((row+1)*H/ROWS)
    for col in range(COLS):
        x0=round(col*W/COLS); x1=round((col+1)*W/COLS)
        TILES.append({'x0':x0,'x1':x1,'y0':y0,'y1':y1,'cx':(x0+x1)/2,'cy':(y0+y1)/2,
            'phase':_rng.uniform(0,2*math.pi),'amplitude':_rng.uniform(.7,1.2),
            'direction':_rng.choice([-1,1]), 'depth':_rng.uniform(.4,1.0)})
_base_bg_cache=None

def smoothstep(x,a,b):
    s=max(0.0,min(1.0,(x-a)/(b-a)))
    return s*s*(3-2*s)

def tile_mosaic(src,t):
    global _base_bg_cache
    # One cinematic split, gently oscillate, then reassemble.
    E=smoothstep(t,.15,1.25)*(1-smoothstep(t,4.75,5.9))
    if E < .001:return src.copy()
    if _base_bg_cache is None:
        blur=cv2.GaussianBlur(src,(0,0),4.0)
        _base_bg_cache=np.clip(blur.astype(np.float32)*.40,0,255).astype(np.uint8)
    bg=np.clip(src.astype(np.float32)*(1-E)+_base_bg_cache.astype(np.float32)*E,0,255).astype(np.uint8)
    for i,tile in enumerate(TILES):
        x0,x1,y0,y1=tile['x0'],tile['x1'],tile['y0'],tile['y1']
        crop=src[y0:y1,x0:x1]
        ht,wt=crop.shape[:2]
        phase=tile['phase']; dep=tile['depth']
        # Controlled independent oscillation, with slight row/column correlated ripple.
        dx=E*(4.5*math.sin(1.65*t+phase)+4.2*math.cos(.95*t+tile['cy']*.027)+2.5*math.sin(2*t+tile['cx']*.009))*dep
        dy=E*(4.2*math.cos(1.2*t+phase)+5.6*math.sin(1.55*t+tile['cx']*.012))*dep
        angle=E*(4.8*math.sin(1.42*t+phase)+2.0*math.cos(2.2*t+phase*.9))
        scale=1-E*(.085+.025*dep)
        # Crop rotates and scales within a local patch: no whole-frame camera motion.
        PS=int(max(wt,ht)*1.55)
        M=cv2.getRotationMatrix2D((wt/2,ht/2),angle,scale)
        M[0,2]+=(PS-wt)/2
        M[1,2]+=(PS-ht)/2
        small=cv2.warpAffine(crop,M,(PS,PS),flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0))
        alpha=cv2.warpAffine(np.full((ht,wt),255,np.uint8),M,(PS,PS),
                             flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=0)
        # Local target coordinates and safe intersection with frame.
        px=round(tile['cx']+dx-PS/2);py=round(tile['cy']+dy-PS/2)
        xa=max(0,px);xb=min(W,px+PS);ya=max(0,py);yb=min(H,py+PS)
        if xa>=xb or ya>=yb:continue
        xx0=xa-px;xx1=xb-px;yy0=ya-py;yy1=yb-py
        tileimg=small[yy0:yy1,xx0:xx1]
        a=alpha[yy0:yy1,xx0:xx1].astype(np.float32)/255
        # Tiny drop shadow to separate floating tiles from the recessed image plane.
        if E>.10:
            sh=cv2.GaussianBlur(alpha,(0,0),2.6)
            xsh=max(0,min(W-1,px+3)); ysh=max(0,min(H-1,py+4))
            sx1=min(W,xsh+PS);sy1=min(H,ysh+PS)
            sw=sx1-xsh; shh=sy1-ysh
            if sw>0 and shh>0:
                srcx=max(0,-(px+3));srcy=max(0,-(py+4))
                if srcy+shh<=PS and srcx+sw<=PS:
                    shadow=sh[srcy:srcy+shh,srcx:srcx+sw].astype(np.float32)/255
                    bg[ysh:sy1,xsh:sx1]=np.clip(bg[ysh:sy1,xsh:sx1].astype(np.float32)*(1-.23*E*shadow[:,:,None]),0,255).astype(np.uint8)
        region=bg[ya:yb,xa:xb]
        bg[ya:yb,xa:xb]=np.clip(region.astype(np.float32)*(1-a[:,:,None])+tileimg.astype(np.float32)*a[:,:,None],0,255).astype(np.uint8)
    return bg

def rhythmic_zoom(src,t):
    # Two perfectly steady in/out cycles over 6 seconds. No color or luminance pulse.
    scale=1.0+0.17*(1-math.cos(2*math.pi*t/3.0))/2
    tw=int(round(W*scale));th=int(round(H*scale))
    big=cv2.resize(src,(tw,th),interpolation=cv2.INTER_CUBIC)
    ox=(tw-W)//2;oy=(th-H)//2
    return big[oy:oy+H,ox:ox+W].copy()
