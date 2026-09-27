"""Finish the lemon-chairs hero: take Gemini TAKE-04 (brunette mic correct), remove the stray arm mic,
clip a true-scale Cloud mic to the blonde's halter neckline. Writes DUET-HERO-LEMON-CHAIRS-CLOUD-MASTER.png"""
import sys, numpy as np
from PIL import Image, ImageFilter
T=Image.open('WORKING/TAKE-04.jpg') if not __import__('os').path.exists('TAKE-04.png') else Image.open('TAKE-04.png').convert('RGB'); W,H=T.size; s=W/2000
O=Image.open('POTENTIAL-HEADER-SHOT-SOURCE.jpg').convert('RGB').resize((W,H),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,60,2))
cx,cy,ang,hgt=[float(v) for v in (sys.argv[1:5] if len(sys.argv)>4 else (1042,478,12,104))]
# 1. remove Gemini's arm mic with the original's clean arm/background
box=[int(v*s) for v in (1165,430,1260,585)]
m=Image.new('L',(W,H),0); m.paste(255,box); m=m.filter(ImageFilter.GaussianBlur(10*s))
T=Image.composite(O,T,m)
# 2. Cloud mic cutout (front, cap on) from the product cutout
k=Image.open('../PRODUCT-PHOTOS/kit-cloud.png').convert('RGBA').crop((85,0,304,910)); k=k.crop(k.getbbox())
h=int(hgt*s); w=int(k.width*h/k.height); mic=k.resize((w,h),Image.LANCZOS)
a=np.asarray(mic).astype(np.float32)/255; rgb=a[...,:3]; al=a[...,3:4]; al=np.where(al<0.35,0,al)
x=np.linspace(0,1,w)[None,:,None]; rgb=rgb*(0.90+0.10*x)                 # window light from camera right
yy=np.linspace(0,1,h)[:,None,None]; rgb=rgb*(1.0-0.04*yy)
rgb=rgb*np.array([0.985,0.955,0.93])                                      # warm the whites to sit with skin
rgb=np.clip(rgb,0,0.955)
rgb=np.clip(rgb+np.random.default_rng(3).normal(0,0.012,(h,w,1)),0,1)                    # photo grain
mic=Image.fromarray((np.concatenate([rgb,al],2)*255).astype(np.uint8),'RGBA').filter(ImageFilter.GaussianBlur(0.6)).rotate(ang,Image.BICUBIC,expand=True)
# 3. contact shadow falls left/down, away from the window
PAD=int(40*s); sa=Image.new('L',(mic.width+2*PAD,mic.height+2*PAD),0); sa.paste(mic.getchannel('A').point(lambda v:int(v*0.30)),(PAD,PAD))
sh=Image.new('RGBA',sa.size,(40,24,30,0)); sh.putalpha(sa.filter(ImageFilter.GaussianBlur(5*s)))
px,py=int(cx*s-mic.width/2),int(cy*s-mic.height/2)
base=T.convert('RGBA'); base.alpha_composite(sh,(px-PAD-int(4*s),py-PAD+int(3*s))); base.alpha_composite(mic,(px,py))
out=base.convert('RGB')
# 4. grain + softness were matched on the mic itself (see step 2)
out.save('DUET-HERO-LEMON-CHAIRS-CLOUD-MASTER.png')
out.crop([int(v*s) for v in (900,330,1300,640)]).resize((800,620)).save('/tmp/claude-0/-home-user-ARC-REPOS/00150b4b-793a-515e-884e-50e331ae2575/scratchpad/blonde_mic.jpg')
print('ok',out.size)
