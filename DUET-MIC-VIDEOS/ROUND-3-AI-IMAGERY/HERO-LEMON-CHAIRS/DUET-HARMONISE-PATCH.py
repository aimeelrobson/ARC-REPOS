"""Gemini pass on a 4:3 patch around the blonde's clipped mic only: make it photographic, keep position/size. Pasted back with a soft mask."""
import json,base64,urllib.request,io,time,numpy as np
from PIL import Image, ImageFilter
M=Image.open('DUET-HERO-LEMON-CHAIRS-CLOUD-MASTER.png').convert('RGB'); s=M.width/2000
cx,cy=1042,478; pw,ph=1320,990; box=(int(cx*s-pw/2),int(cy*s-ph/2)); box=box+(box[0]+pw,box[1]+ph)
patch=M.crop(box); buf=io.BytesIO(); patch.save(buf,'PNG')
ref=open('../PRODUCT-PHOTOS/REF-MIC-CLOUD-FRONT.png','rb').read()
P=("This is a close crop of a real photograph. The small white wireless microphone clipped to the woman's floral halter top was pasted in and looks flat. "
"Re-render ONLY that microphone so it looks like a real photographed object in this scene: subtle 3D shading with soft window light from the right, a gentle highlight on the right edges, "
"its clip visibly gripping the edge of the floral fabric, and a soft natural contact shadow on the skin and fabric. "
"Keep its EXACT position, size, angle and design (white foam cap on top, one rounded-square button, one tiny green LED dot above the button, small side tabs) — match the second image. "
"Do not change anything else: skin, face, hair, fabric pattern, background and colours must stay identical. No text, no logos.")
body={"contents":[{"parts":[{"inline_data":{"mime_type":"image/png","data":base64.b64encode(buf.getvalue()).decode()}},{"inline_data":{"mime_type":"image/png","data":base64.b64encode(ref).decode()}},{"text":P}]}],
      "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"4:3","imageSize":"2K"}}}
for n in range(3):
    for a in range(4):
        try: d=json.load(urllib.request.urlopen(urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=300)); break
        except urllib.error.HTTPError as e:
            if e.code in (429,500,503): time.sleep(20*(a+1)); continue
            raise
    for c in d.get('candidates',[]):
        for p in c.get('content',{}).get('parts',[]):
            if 'inlineData' in p: Image.open(io.BytesIO(base64.b64decode(p['inlineData']['data']))).convert('RGB').resize((pw,ph),Image.LANCZOS).save(f'PATCH-{n+1:02d}.png')
    print('patch',n+1,'done',flush=True)
json.dump({'box':box},open('patch_box.json','w'))
