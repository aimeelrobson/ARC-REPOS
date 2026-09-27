"""Move the blonde's mic from her neckline into her raised hand (held, like the brunette). Gemini on a square patch only; pasted back softly."""
import json,base64,urllib.request,io,time,sys
from PIL import Image
M=Image.open('DUET-HERO-LEMON-CHAIRS-CLOUD-MASTER.png').convert('RGB'); s=M.width/2000
O=Image.open('POTENTIAL-HEADER-SHOT-SOURCE.jpg').convert('RGB')
cx,cy,half=1120,400,215                      # covers neckline mic + raised hand
box=tuple(int(v*s) for v in (cx-half,cy-half,cx+half,cy+half))
def enc(im):
    b=io.BytesIO(); im.save(b,'PNG'); return {"inline_data":{"mime_type":"image/png","data":base64.b64encode(b.getvalue()).decode()}}
patch=M.crop(box); orig=O.crop((cx-half,cy-half,cx+half,cy+half)).resize(patch.size,Image.LANCZOS)
ref=Image.open('../PRODUCT-PHOTOS/REF-MIC-CLOUD-FRONT.png')
P=("Edit the FIRST image, a close crop of a real photograph. "
"1) REMOVE the small white microphone clipped to the floral top at her neckline; restore the floral fabric strap and skin underneath naturally. "
"2) Put a white wireless microphone PINCHED between the thumb and index finger of her raised hand, exactly where the small black microphone is held in the SECOND image (same position, same size, same grip) — "
"but white, matching the THIRD image exactly: white foam cap on top, one rounded-square button, one tiny green LED dot above the button, small side tabs. Front toward the camera, upright. "
"Keep it tiny: no longer than her index finger. Fingers overlap it naturally. Soft window light from the right, gentle contact shadow on the fingers. "
"Change NOTHING else: face, sunglasses, hair, hand shape, fabric pattern, background and colours stay identical. No text, no logos.")
out=[]
for n in range(int(sys.argv[1]) if len(sys.argv)>1 else 3):
    body={"contents":[{"parts":[enc(patch),enc(orig),enc(ref),{"text":P}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1","imageSize":"2K"}}}
    for a in range(4):
        try: d=json.load(urllib.request.urlopen(urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=300)); break
        except urllib.error.HTTPError as e:
            if e.code in (429,500,503): time.sleep(20*(a+1)); continue
            raise
    for c in d.get('candidates',[]):
        for p in c.get('content',{}).get('parts',[]):
            if 'inlineData' in p: Image.open(io.BytesIO(base64.b64decode(p['inlineData']['data']))).convert('RGB').resize(patch.size,Image.LANCZOS).save(f'HELD-{n+1:02d}.png')
    print('held',n+1,flush=True)
json.dump({'box':box},open('held_box.json','w'))
c=Image.new('RGB',(4*420,420),'white'); c.paste(patch.resize((420,420)),(0,0))
for n in range(3):
    try: c.paste(Image.open(f'HELD-{n+1:02d}.png').resize((420,420)),(420*(n+1),0))
    except Exception: pass
c.save('/tmp/claude-0/-home-user-ARC-REPOS/00150b4b-793a-515e-884e-50e331ae2575/scratchpad/held.jpg')
