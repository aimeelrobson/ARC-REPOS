"""Extend the lemon-chairs master into (a) a zoomed-out desktop hero with lilac room for the headline on the left,
(b) a 4:5 mobile hero. Gemini paints the new room; the master is pasted back over its own area so people/mics stay exact."""
import sys,json,base64,urllib.request,io,time
from PIL import Image, ImageFilter
M=Image.open('DUET-HERO-LEMON-CHAIRS-CLOUD-MASTER.png').convert('RGB'); W,H=M.size
def ask(canvas,aspect,prompt,out):
    small=canvas.copy(); small.thumbnail((2400,2400)); buf=io.BytesIO(); small.save(buf,'JPEG',quality=92)
    body={"contents":[{"parts":[{"inline_data":{"mime_type":"image/jpeg","data":base64.b64encode(buf.getvalue()).decode()}},{"text":prompt}]}],
          "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":aspect,"imageSize":"4K"}}}
    for a in range(4):
        try: d=json.load(urllib.request.urlopen(urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=400)); break
        except urllib.error.HTTPError as e:
            if e.code in (429,500,503): time.sleep(20*(a+1)); continue
            raise
    for c in d['candidates']:
        for p in c['content']['parts']:
            if 'inlineData' in p: Image.open(io.BytesIO(base64.b64decode(p['inlineData']['data']))).convert('RGB').resize(canvas.size,Image.LANCZOS).save(out); return out
P=("This photograph has been placed on a larger canvas; the flat mid-grey areas are EMPTY and must be filled. "
   "Extend the same bright lilac photo studio room naturally into the grey areas: {what}. Seamless continuation of the existing walls, floor, light and soft shadows, "
   "same colour grade, same softness and grain. Keep everything already in the photo exactly as it is — same people, pose, mics, chairs, framing. "
   "Do not add people, objects, furniture, text or logos in the new areas: calm, empty lilac space.")
def build(kind):
    if kind=='desktop':
        T=int(0.55*H); L=int(T*W/H); cw,ch=W+L,H+T; ox,oy=L,T; aspect='16:9'
        what='more lilac wall and ceiling above, and more empty lilac room with a plain wall and smooth floor to the LEFT'
    else:
        cw=int(W*0.96); ch=int(cw*5/4); ox=int(-W*0.03); oy=int(ch*0.28); aspect='4:5'
        what='more lilac wall above the two women, and below them the rest of the two yellow moulded shell chairs with their thin light-wood/wire Eiffel-style legs standing on a smooth lilac floor'
    cv=Image.new('RGB',(cw,ch),(128,128,128)); cv.paste(M,(ox,oy))
    gen=ask(cv,aspect,P.format(what=what),f'EXT-{kind.upper()}-RAW.png')
    g=Image.open(gen).convert('RGB')
    m=Image.new('L',(cw,ch),0); inset=int(0.02*W); m.paste(255,(max(ox,0)+inset,oy+inset,min(ox+W,cw)-(inset if ox+W<=cw else 0),min(oy+H,ch)-(inset if oy+H<ch else 0)))
    m=m.filter(ImageFilter.GaussianBlur(inset*0.6))
    out=Image.composite(cv,g,m); out.save(f'EXT-{kind.upper()}.png'); print(kind,out.size,flush=True)
for k in (sys.argv[1:] or ['desktop','mobile']): build(k)
