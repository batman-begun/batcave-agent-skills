"""User-approved v0.4b: steep shadow, sixfold snow, blue hex-bokeh, sunbeam."""
from __future__ import annotations
import cv2, numpy as np, math, random
W,H=854,480
XX,YY=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
RNG=random.Random(20261118)

def init_particles(count):
    a=[]
    for i in range(count):
        depth=RNG.random()
        a.append(dict(x=RNG.uniform(-90,W+90),y=RNG.uniform(-H,H),d=depth,phase=RNG.random()*7,
          speed=RNG.uniform(.6,1.5),size=RNG.uniform(.72,1.3),swing=RNG.uniform(3,22),seed=i,
          vx=RNG.uniform(-1.0,1.0),vy=RNG.uniform(-1.0,1.0)))
    return a

SNOW=init_particles(210)
BOKEH=init_particles(21)
DUST=init_particles(95)
SHADOW_BANDS=[]

def init_shadow_bands():
    rng=random.Random(4260)
    angle_deg=60
    m=math.tan(math.radians(angle_deg))  # y = m x ; for band generation in x(y)
    for z in range(3):
        layer=[]
        spacing=150-15*z
        width=52-8*z
        x0=-420 + z*18
        while x0 < W+460:
            layer.append((x0 + rng.randint(-18,18), width + rng.randint(-8,10), m*(.90+.08*z)))
            x0 += spacing + rng.randint(-10,10)
        SHADOW_BANDS.append(layer)

init_shadow_bands()

def shadow_reveal(base,t):
    mask=np.zeros((H,W),np.float32)
    for z,layer in enumerate(SHADOW_BANDS):
        ly=np.zeros((H,W),np.float32)
        # slower foreground, slightly drifting background
        driftx= int((18-4*z)*t + 14*math.sin(t*.55+z*1.1))
        drifty= int(5*math.sin(t*.81+z*0.8))
        for xbase,width,m in layer:
            # band centerline: x = xbase + m*y + driftx
            for yi in range(H):
                x = int(xbase + (yi+drifty)*0.58/m + driftx)  # invert to make steeper perceived angle
                xa=max(0,x-width//2); xb=min(W,x+width//2)
                if xb>xa: ly[yi,xa:xb]=1.0
        ly=cv2.GaussianBlur(ly,(0,0),5+z*4)
        mask=np.maximum(mask, ly*(0.78-z*0.14))
    s=np.clip(mask,0,1)[:,:,None]
    bright=((1-s)*(.03+.015*np.sin(t*.7)))
    out=np.clip(base.astype(np.float32)*(1-.72*s)+255*bright,0,255).astype(np.uint8)
    return out

def draw_snowflake(img,x,y,r,color,alpha_scale=1.0):
    if r <= 1.4:
        cv2.circle(img,(int(x),int(y)),1,color,-1,cv2.LINE_AA)
        return
    arms=6
    for k in range(arms):
        a=math.radians(60*k)
        dx=math.cos(a)*r; dy=math.sin(a)*r
        x2=int(round(x+dx)); y2=int(round(y+dy))
        cv2.line(img,(int(x),int(y)),(x2,y2),color,1,cv2.LINE_AA)
        # side branches only on near flakes
        if r >= 2.1:
            bx=x+dx*.58; by=y+dy*.58
            b1=a+math.radians(30); b2=a-math.radians(30)
            s=max(1.0,r*.28)
            cv2.line(img,(int(round(bx)),int(round(by))),(int(round(bx+math.cos(b1)*s)),int(round(by+math.sin(b1)*s))),color,1,cv2.LINE_AA)
            cv2.line(img,(int(round(bx)),int(round(by))),(int(round(bx+math.cos(b2)*s)),int(round(by+math.sin(b2)*s))),color,1,cv2.LINE_AA)

def snow_dust(base,t):
    im=cv2.convertScaleAbs(base,alpha=.86,beta=6)
    far=np.zeros_like(im); near=np.zeros_like(im)
    for p in SNOW:
        z=p['d']; speed=(32+82*z)*p['speed']
        gust=(10+24*z)*math.sin(t*.63+p['phase']*.7)
        x=(p['x']+gust+6*math.sin(t*(.52+p['speed'])+p['phase']))%(W+50)-25
        y=(p['y']+t*speed)%(H+70)-35
        r=(.7+2.05*z)*(.70+.35*p['size'])
        if z<.42:
            draw_snowflake(far,x,y,r,(190,204,218))
        else:
            draw_snowflake(near,x,y,r,(245,249,253))
    far=cv2.GaussianBlur(far,(0,0),0.85)
    near=cv2.GaussianBlur(near,(0,0),0.25)
    out=cv2.addWeighted(im,1,far,.62,0)
    out=cv2.addWeighted(out,1,near,.85,0)
    return out

def hex_points(x,y,r,rot=0.0):
    pts=[]
    for i in range(6):
        a=rot+math.radians(60*i+30)  # flat-ish top aperture
        pts.append((int(round(x+math.cos(a)*r)), int(round(y+math.sin(a)*r))))
    return np.array(pts,np.int32)

def bokeh(base,t):
    out=cv2.convertScaleAbs(base,alpha=.84,beta=-5)
    glow=np.zeros_like(out)
    core=np.zeros_like(out)
    for p in BOKEH:
        z=p['d']
        rr=int((8+22*z)*(.82+.28*p['size'])*(.94+.06*math.sin(t*.72+p['phase'])))
        x=(p['x']+t*(20+30*z)+18*math.sin(t*.43+p['phase']))%(W+2*rr)-rr
        y=(p['y']-t*(12+18*z)+7*math.cos(t*.48+p['phase']))%(H+2*rr)-rr
        rot=t*(.06+.08*z)+p['phase']*.15
        col=[(178,214,255),(146,198,250),(166,220,255),(200,224,248)][p['seed']%4]
        pts=hex_points(x,y,rr,rot)
        pts2=hex_points(x,y,int(rr*1.28),rot)
        cv2.fillConvexPoly(glow,pts2,col,cv2.LINE_AA)
        cv2.fillConvexPoly(core,pts,tuple(int(v*.18) for v in col),cv2.LINE_AA)
        cv2.polylines(core,[pts],True,col,1,cv2.LINE_AA)
    glow=cv2.GaussianBlur(glow,(0,0),10)
    core=cv2.GaussianBlur(core,(0,0),1.6)
    out=cv2.addWeighted(out,1,glow,.28,0)
    out=cv2.addWeighted(out,1,core,.52,0)
    return out

BEAM_DIRS=[(.16,.032,1.00),(.43,-.038,.78),(.74,.026,1.14)]

def sunbeam(base,t):
    F=base.astype(np.float32)*.73  # darker base -> more contrast
    rays=np.zeros((H,W),np.float32)
    for i,(center,drift,weight) in enumerate(BEAM_DIRS):
        xc=W*(center+drift*(6.8*math.sin(t/6.8))*1.8)+YY*(.27+.078*i)
        distance=XX-xc
        thickness=W*(.058+.021*i)
        envelope=(.74*np.exp(-.5*(distance/thickness)**2) + .58*np.exp(-.5*((distance)/(thickness*.34))**2))
        pulse=.84+.21*np.sin(t*(.67+.12*i)+i*.7)
        rays += weight*envelope*pulse
    rays=np.clip(rays,0,1.95)
    buff=np.empty_like(F)
    buff[:,:,0]=F[:,:,0]*(1+.08*rays)+54*rays
    buff[:,:,1]=F[:,:,1]*(1+.14*rays)+74*rays
    buff[:,:,2]=F[:,:,2]*(1+.24*rays)+98*rays
    out=np.clip(buff,0,255).astype(np.uint8)
    # dust with randomized curved paths, clearer but not bigger: mostly 1px, occasional 2px for nearest
    for p in DUST:
        x=int((p['x'] + t*(5+11*p['d']) + 8*math.sin(t*(.7+.2*p['vy']) + p['phase']) + 5*math.sin(t*1.9+p['seed'])) % W)
        y=int((p['y'] - t*(10+16*p['d']) + 4*math.cos(t*(.95+.15*p['vx']) + p['phase']*1.3) + 3*math.sin(t*1.37+p['seed']*.2)) % H)
        if rays[y,x] > .16:
            col=(205,228,248) if p['d']>.5 else (185,212,238)
            rad=1 if p['d']<.92 else 2
            cv2.circle(out,(x,y),rad,col,-1,cv2.LINE_AA)
    return out
