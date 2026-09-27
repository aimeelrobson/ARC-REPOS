"""Remove tone seams between Gemini's extended room and the pasted master: low-frequency colour correction spread outward, then a wide feather."""
import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter as gf
M=Image.open('DUET-HERO-LEMON-CHAIRS-CLOUD-MASTER.png').convert('RGB'); W,H=M.size
R=Image.open('EXT-DESKTOP-RAW.png').convert('RGB'); cw,ch=R.size; T=int(0.55*H); L=int(T*W/H)
cv=Image.new('RGB',(cw,ch)); cv.paste(M,(L,T))
k=8; sw,sh=cw//k,ch//k
r=np.asarray(R.resize((sw,sh),Image.BILINEAR),np.float32); c=np.asarray(cv.resize((sw,sh),Image.BILINEAR),np.float32)
inside=np.zeros((sh,sw),np.float32); inside[T//k+4:,L//k+4:]=1
def blur(a,s): return np.asarray(Image.fromarray(a).filter(ImageFilter.GaussianBlur(s))) if a.ndim==2 else np.stack([blur(a[...,i],s) for i in range(a.shape[2])],2)
D=(c-r)*inside[...,None]
num=np.stack([gf(D[...,i],40) for i in range(3)],2)
den=gf(inside,40)[...,None]
Ds=num/np.maximum(den,1e-3)
# fade the correction out with distance from the master
dist=gf(inside,120); fade=np.clip(dist*2.2,0,1)[...,None]
corr=Ds*fade
corrF=np.stack([np.asarray(Image.fromarray(corr[...,i].astype(np.float32)).resize((cw,ch),Image.BILINEAR)) for i in range(3)],2)
R2=Image.fromarray(np.clip(np.asarray(R,np.float32)+corrF,0,255).astype(np.uint8))
m=Image.new('L',(cw,ch),0); f=int(0.05*W); m.paste(255,(L+f,T+f,cw,ch)); m=m.filter(ImageFilter.GaussianBlur(f*0.5))
cv2=R2.copy(); cv2.paste(M,(L,T)); out=Image.composite(cv2,R2,m); out.save('EXT-DESKTOP.png'); print('ok',out.size)
a=out; c2=Image.new('RGB',(1600,444)); c2.paste(a.crop((L-900,T-500,L+900,T+500)).resize((800,444)),(0,0)); c2.paste(a.crop((L+1800,T-500,L+3600,T+500)).resize((800,444)),(800,0))
c2.save('/tmp/claude-0/-home-user-ARC-REPOS/00150b4b-793a-515e-884e-50e331ae2575/scratchpad/seams.jpg')
