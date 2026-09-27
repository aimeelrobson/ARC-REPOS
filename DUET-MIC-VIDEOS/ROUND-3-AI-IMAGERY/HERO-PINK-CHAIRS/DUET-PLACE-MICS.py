"""Step 2 (usage: SCALE TAG, e.g. 1.0 TRUE or 1.3 HERO): place the real Cloud cutout at true scale (6.5 cm ~ 23 px/cm on the master) with a flash drop shadow."""
from PIL import Image, ImageFilter, ImageChops
W='WORKING/'
cut=Image.open(W+'CLOUD-CUTOUT.png')
# side: (nomic patch, target height px, rotation deg, centre x,y in patch coords)
JOBS={'L':('NOMIC-L-02.png',135,-28,(360,440)),'R':('NOMIC-R-01.png',160,-4,(470,470))}
import sys
K=float(sys.argv[1]) if len(sys.argv)>1 else 1.0; tag=sys.argv[2] if len(sys.argv)>2 else 'TRUE'
for side,(src,h,rot,(cx,cy)) in JOBS.items():
    h=int(h*K)
    base=Image.open(W+src).convert('RGB')
    m=cut.resize((int(cut.width*h/cut.height),h),Image.LANCZOS).rotate(rot,expand=True,resample=Image.BICUBIC)
    x,y=cx-m.width//2,cy-m.height//2
    # drop shadow: blurred alpha, offset down-right, multiplied into the fabric
    sh=Image.new('L',base.size,0); sh.paste(m.split()[3],(x+9,y+12)); sh=sh.filter(ImageFilter.GaussianBlur(7)).point(lambda v:int(v*0.55))
    dark=ImageChops.multiply(base,Image.new('RGB',base.size,(70,40,60)))
    out=Image.composite(dark,base,sh); out.paste(m,(x,y),m)
    out.save(W+f'PLACED-{side}-{tag}.png')
