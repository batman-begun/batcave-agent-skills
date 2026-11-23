"""Approved v0.4 flowing-water, rain-glass and sakura particle implementations."""
from __future__ import annotations
import cv2, numpy as np, math, random
W,H=854,480
XX,YY=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
RNG=random.Random(20261118)

def init_particles(count,mode):
    a=[]
    for i in range(count):
        depth=RNG.random()
        a.append(dict(x=RNG.uniform(-90,W+90),y=RNG.uniform(-H,H),d=depth,phase=RNG.random()*7,
          speed=RNG.uniform(.6,1.5),size=RNG.uniform(.72,1.3),swing=RNG.uniform(3,22),seed=i))
    return a

RAIN_STREAKS=init_particles(350,'rain')
RAIN_DROPS=init_particles(48,'drop')
# Advance the deterministic RNG exactly as in approved v0.4 prototype, so
# sakura trajectories remain identical despite the unused snow field.
_unused_snow=init_particles(255,'snow')
PETALS=init_particles(64,'petals')

def water_mirage(base,t):
    yphase=YY-(41*t+8*np.sin(t*.57)) + XX*.055
    band1=np.exp(-((((yphase-155+500)%1000)-500)/125)**2)
    band2=np.exp(-((((yphase-415+500)%1000)-500)/85)**2)
    d1=(10.5*np.sin(yphase/20+1.1*np.sin(XX/136+t*.53))+5.4*np.sin(yphase/47-XX/95+t*.27))*band1
    d2=7.5*np.sin((YY+XX*.11+29*t)/16)*band2
    mx=XX+d1+d2
    my=YY+3.7*np.sin(yphase/29-XX*.013)*band1+2*np.cos(yphase/38)*band2
    return cv2.remap(base,mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)

def rain_glass(base,t):
    # Distant rainfall, uneven speeds; near-glass beads distort only their own local pixels.
    img=cv2.convertScaleAbs(base,alpha=.82,beta=-3)
    streak=np.zeros_like(img)
    for p in RAIN_STREAKS:
        z=p['d'];v=370+450*z
        x=int((p['x']-t*38*(.5+z)+W*2)%(W+110)-55)
        y=int((p['y']+t*v)%(H+100)-50)
        ln=int(6+19*z*p['size'])
        shade=130+int(50*z)
        cv2.line(streak,(x,y),(x-2-int(z*3),y+ln),(shade+7,shade+4,shade),1 if z<.85 else 2,cv2.LINE_AA)
    img=cv2.addWeighted(img,1,streak,.40,0)
    # Large foreground beads carry a bright curved rim and a tiny refractive offset.
    for p in RAIN_DROPS:
        x=int((p['x']+8*math.sin(t*.75+p['phase']))%W)
        y=int((p['y']+t*(15+47*p['d'])*p['speed'])%(H+85)-35)
        r=int(3+5.5*p['d']*p['size'])
        if not 0<y<H-40 or x<r+3 or x>W-r-4:continue
        # local droplet lens, never global displacement
        xa,xb=x-r-1,x+r+2; ya,yb=max(0,y-r*2),min(H-35,y+r*2)
        patch=img[ya:yb,xa:xb].copy()
        if len(patch)>2:
            ph,pw=patch.shape[:2]
            yp,xp=np.mgrid[:ph,:pw].astype(np.float32)
            warp=cv2.remap(patch,xp+1.1*np.sin(yp/(ph+1)*np.pi),yp-.7,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT_101)
            img[ya:yb,xa:xb]=cv2.addWeighted(patch,.57,warp,.43,0)
        cv2.line(img,(x,y-3*r),(x-1,y-1*r),(95,107,121),1,cv2.LINE_AA)
        cv2.ellipse(img,(x,y),(max(3,r),max(5,int(1.25*r))),0,180,340,(164,189,216),1,cv2.LINE_AA)
        cv2.line(img,(x-r//2,y-1),(x-r//2,y+r//2),(210,227,246),1,cv2.LINE_AA)
        cv2.circle(img,(x+int(r*.45),y-int(r*.35)),1,(221,232,247),-1,cv2.LINE_AA)
    return img

def petal_polygon(cx,cy,theta,scale,flip):
    base=np.array([(0,-1.15),(-.29,-1.02),(-.72,-.92),(-.89,-.53),(-.85,-.1),(-.58,.36),(0,1.0),(.58,.36),(.85,-.1),(.89,-.53),(.72,-.92),(.29,-1.02)],dtype=np.float32)
    base[:,0]*=flip
    co,si=math.cos(theta),math.sin(theta)
    M=np.array([[co,-si],[si,co]],np.float32)
    return np.rint(base@M.T*scale+np.array([cx,cy])).astype(np.int32)

def petals(base,t):
    out=base.copy()
    soft=np.zeros_like(out)
    cols=[(185,155,244),(210,172,250),(212,190,252),(182,129,235)]
    for p in PETALS:
        z=p['d']; sw=15+43*z
        x=int((p['x']+t*(34+30*z)+25*math.sin(t*1.5+p['phase'])+5*t*t)%(W+110)-55)
        y=int((p['y']+t*(43+75*z)*p['speed']+12*math.cos(t*.9+p['phase']))%(H+110)-55)
        theta=p['phase']+t*(.6+1.5*z)*p['speed']
        flip=.40+.6*abs(math.cos(theta*.79))
        size=(6+10*z)*p['size']
        if z>.72:size*=1.4
        poly=petal_polygon(x,y,theta,size,flip)
        color=cols[p['seed']%len(cols)]
        cv2.fillPoly(soft,[poly],color,cv2.LINE_AA)
        cv2.polylines(soft,[poly],True,(150,125,190),1,cv2.LINE_AA)
        px=int(x-size*.23*math.sin(theta));py=int(y+size*.25*math.cos(theta))
        cv2.line(soft,(x,y+int(size*.6)),(px,py), (175,147,210),1,cv2.LINE_AA)
    # enhance visibility without making an opaque giant pink sheet
    return cv2.addWeighted(out,.93,soft,.86,0)
