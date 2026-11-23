"""Supplemental approved cinematic motion effects for FFMD v0.4.
Frame functions accept BGR uint8 image (480x854) and time in seconds.
No camera drift except rhythmic_zoom and cinematic_impact.
"""
from __future__ import annotations
import math, random
import cv2
import numpy as np
W,H=854,480
XX,YY=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
CX,CY=(W-1)/2,(H-1)/2
RAD=np.maximum(1,np.sqrt((XX-CX)**2+(YY-CY)**2))
RX,RY=np.meshgrid(np.arange(W//2,dtype=np.float32),np.arange(H//2,dtype=np.float32))
RCX,RCY=(W//2)/2,(H//2)/2
RR=np.maximum(1,np.hypot(RX-RCX, RY-RCY))
RNG=random.Random(8110902)
EMBERS=[(RNG.uniform(0,W),RNG.uniform(0,H),RNG.random(),RNG.uniform(0,math.tau)) for _ in range(195)]


def radial_refraction(base,t):
    # Reproduces approved Cinematic sample, pure concentric pixel refraction.
    half=cv2.resize(base,(W//2,H//2),interpolation=cv2.INTER_AREA)
    phase=RR-110*(t%4)
    a=7.0*np.sin(2*np.pi*phase/38)*np.exp(-(phase/55)**2)
    mx=RX+a*(RX-RCX)/RR
    my=RY+a*(RY-RCY)/RR
    warped=cv2.remap(half,mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)
    return cv2.resize(warped,(W,H),interpolation=cv2.INTER_CUBIC)


def prism_glass(base,t):
    # Local pixel displacement through faceted moving panes, NOT only polygons.
    out=base.copy()
    polys=[((-110,-60),(190,30),(130,370),(-170,310)),
           ((410,-90),(790,50),(640,290),(320,200)),
           ((140,240),(440,195),(620,500),(260,560))]
    cols=[(238,175,92),(146,104,233),(195,213,240)]
    for i,points in enumerate(polys):
        shiftx=round(48*np.sin(t*.43+i*1.8)+t*(6-3*i))
        shifty=round(22*np.cos(t*.41+i*.7))
        pts=np.array(points,np.int32)+[shiftx,shifty]
        mask=np.zeros((H,W),np.uint8)
        cv2.fillConvexPoly(mask,pts,255)
        mask=cv2.GaussianBlur(mask,(0,0),5.0)
        alpha=(mask.astype(np.float32)/255*.56)[:,:,None]
        dx=round(8*np.sin(.73*t+i*.8)) + (5 if i==0 else -4)
        dy=round(5*np.cos(.61*t+i*.7))
        moved=cv2.warpAffine(base,np.float32([[1,0,dx],[0,1,dy]]),(W,H),borderMode=cv2.BORDER_REFLECT_101)
        toned=np.clip(moved.astype(np.float32)*np.array([1.05,.96,1.1]) +np.array(cols[i])*0.09,0,255)
        out=np.clip(out.astype(np.float32)*(1-alpha)+toned*alpha,0,255).astype(np.uint8)
        cv2.polylines(out,[pts],True,cols[i],1,cv2.LINE_AA)
    return out


def cyber_glitch(base,t):
    out=base.copy()
    # Four localized glitch clusters, visibly tearing but not continuously flashing.
    windows=(4.0,10.8,18.2,25.0)
    at=min(abs(t-w) for w in windows)
    if at>.42: return out
    p=max(0,(.42-at)/.42)
    step=int(t*24)
    rng=random.Random(4804+step//3)
    if step%5 == 0: return out  # abrupt intermittent dropout
    for j in range(int(6+14*p)):
        y=rng.randrange(H)
        h=rng.randint(3,28)
        shift=rng.randint(-35,35)
        y2=min(H,y+h)
        band=base[y:y2]
        out[y:y2]=np.roll(band,shift,axis=1)
    b,g,r=cv2.split(out)
    b=np.roll(b,-int(5+11*p),axis=1)
    r=np.roll(r,int(5+11*p),axis=1)
    out=cv2.merge([b,g,r])
    for y in range(step%4,H,6):
        out[y:y+1]=np.clip(out[y:y+1].astype(np.float32)*(.52+.28*(1-p)),0,255).astype(np.uint8)
    return out


def firestorm(base,t):
    warm=base.astype(np.float32)*[.81,.9,1.04]
    warm=np.clip(warm,0,255).astype(np.uint8)
    overlay=np.zeros_like(base)
    for i,(x0,y0,z,phase) in enumerate(EMBERS):
        speed=32+100*z
        x=int((x0+12*np.sin(.9*t+phase)+5*t*z)%(W+24)-12)
        y=int((y0-speed*t)%(H+50)-25)
        r=1+round(2.0*z)
        col=[(11,137,249),(29,192,255),(93,224,255)][i%3]
        cv2.circle(overlay,(x,y),r,col,-1,cv2.LINE_AA)
        if i%4==0:
            cv2.line(overlay,(x,y),(x-2,y+5+r*2),(20,97,197),1,cv2.LINE_AA)
    gl=cv2.GaussianBlur(overlay,(0,0),5)
    out=cv2.addWeighted(warm,1,gl,.35,0)
    return cv2.addWeighted(out,1,overlay,.91,0)


def film_burn(base,t):
    arr=base.astype(np.float32)
    mod=t%8.0
    loc=-.2+(mod/8)*1.5
    # High contrast orange burn that slides across an edge, leaving structure visible.
    dist=np.abs(XX/W-loc)
    leakage=np.exp(-((dist)/.13)**2)
    rim=np.exp(-((dist-.11)/.033)**2)
    shimmer=.82+.16*np.sin(t*5.1)+.08*np.sin(t*13.7)
    a=np.clip((leakage*.57+rim*.35)*shimmer,0,.82)
    burn=np.array([33,114,255],np.float32)[None,None,:]
    out=arr*(1-a[:,:,None])+burn*a[:,:,None]
    out *= (1+.055*np.sin(t*3.3))
    rng=random.Random(20261118+int(t*4))
    for j in range(10):
        x=rng.randint(0,W-1); y=rng.randint(0,H-1)
        if rng.random()<.23:cv2.line(out,(x,y),(x+rng.randint(-2,2),min(H-1,y+rng.randint(15,95))),(138,213,255),1,cv2.LINE_AA)
    return np.clip(out,0,255).astype(np.uint8)


def cinematic_impact(base,t):
    # Two isolated shockbeats; no continuous camera pan.
    bursts=[(8.8,.15),(21.4,.19)]
    strength=max(amp*math.exp(-abs(t-mark)/.27) for mark,amp in bursts)
    if strength<.002:return base.copy()
    z=1+strength
    tw=int(W*z)+2; th=int(H*z)+2
    big=cv2.resize(base,(tw,th),interpolation=cv2.INTER_LINEAR)
    mag=min(18,strength*110)
    sx=int(mag*math.sin(t*77)); sy=int(mag*.7*math.cos(t*93))
    ox=np.clip((tw-W)//2+sx,0,tw-W);oy=np.clip((th-H)//2+sy,0,th-H)
    frame=big[oy:oy+H,ox:ox+W].copy()
    return cv2.convertScaleAbs(frame,alpha=1.0+.14*strength/.19,beta=0)
