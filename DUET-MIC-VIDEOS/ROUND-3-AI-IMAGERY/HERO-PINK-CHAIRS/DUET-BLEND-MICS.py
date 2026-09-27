"""Step 4: blend finished mic patches back into the red master with a feathered mask + edge colour-match."""
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
BOX={'L':(1850,1250,2750,2150),'R':(3030,1150,3930,2050)}
M0=Image.open('DUET-HERO-PINK-CHAIRS-RED-MASTER.png').convert('RGB')
def blend(M,side,patch_file):
    x0,y0,x1,y1=BOX[side]; w,h=x1-x0,y1-y0
    P=np.array(Image.open('WORKING/'+patch_file).convert('RGB')).astype(float)
    O=np.array(M.crop(BOX[side])).astype(float)
    ring=np.zeros((h,w),bool); ring[:60]=ring[-60:]=True; ring[:,:60]=ring[:,-60:]=True
    P=np.clip(P+(O[ring].mean(0)-P[ring].mean(0)),0,255)          # colour-match to surroundings
    mk=Image.new('L',(w,h),0); ImageDraw.Draw(mk).rectangle((90,90,w-90,h-90),fill=255); mk=mk.filter(ImageFilter.GaussianBlur(45))
    M.paste(Image.composite(Image.fromarray(P.astype('uint8')),M.crop(BOX[side]),mk),(x0,y0))
for name,(l,r) in {'CLOUD':('FINAL-L-HERO-PLAIN-2.png','FINAL-R-HERO-PLAIN-3.png'),
                   'CLOUD-MINT':('FINAL-L-HERO-MINT.png','FINAL-R-HERO-MINT.png'),
                   'CLOUD-TRUE-SCALE':('PLACED-L-TRUE.png','PLACED-R-TRUE.png')}.items():
    M=M0.copy(); blend(M,'L',l); blend(M,'R',r)
    M.save(f'DUET-HERO-PINK-CHAIRS-RED-{name}-MASTER.png')
    M.resize((2400,1340),Image.LANCZOS).save(f'duet-pastel-hero-pink-chairs-red-{name.lower()}-web.jpg',quality=86)
    M.resize((1600,893),Image.LANCZOS).save(f'DUET-HERO-PINK-CHAIRS-RED-{name}-PREVIEW.jpg',quality=84)
    print(name)
