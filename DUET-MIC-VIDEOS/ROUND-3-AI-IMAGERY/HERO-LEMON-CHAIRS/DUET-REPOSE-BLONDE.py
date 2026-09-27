"""Re-pose the blonde: raised arm lowered and draped loosely over her other arm, mic dangling from her fingers in front of her denim shorts. Gemini on a 3:4 patch only."""
import json,base64,urllib.request,io,time,sys
from PIL import Image
M=Image.open('DUET-HERO-LEMON-CHAIRS-CLOUD-MASTER.png').convert('RGB'); s=M.width/2000
box=tuple(int(v*s) for v in (930,130,1570,983))
def enc(im):
    b=io.BytesIO(); im.save(b,'PNG'); return {"inline_data":{"mime_type":"image/png","data":base64.b64encode(b.getvalue()).decode()}}
patch=M.crop(box); ref=Image.open('../PRODUCT-PHOTOS/REF-MIC-CLOUD-FRONT.png')
P=("Edit this crop of a real photograph (the blonde woman laughing, back to back with a friend on yellow chairs). Change ONLY her raised arm: "
"lower that arm and let it drape loosely across her body, resting relaxed over her other arm (which stays exactly where it is). She is laughing so hard that her hand hangs limp, "
"and the small white wireless microphone dangles loosely from her fingertips in front of her dark denim shorts, so the white mic stands out clearly against the dark denim. "
"The mic must match the second image exactly: white foam cap on top, one rounded-square button, one tiny green LED, small side tabs; tiny, about the length of her index finger. "
"Fill the lilac background where her raised arm and hand used to be. Keep her face, laugh, sunglasses, hair, floral top, shorts, the chair, lighting (soft window light from the right) and colour grade identical. "
"Anatomy must be natural: correct elbow, wrist and five fingers. No text, no logos.")
for n in range(int(sys.argv[1]) if len(sys.argv)>1 else 3):
    body={"contents":[{"parts":[enc(patch),enc(ref),{"text":P}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"3:4","imageSize":"2K"}}}
    for a in range(4):
        try: d=json.load(urllib.request.urlopen(urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=300)); break
        except urllib.error.HTTPError as e:
            if e.code in (429,500,503): time.sleep(20*(a+1)); continue
            raise
    for c in d.get('candidates',[]):
        for p in c.get('content',{}).get('parts',[]):
            if 'inlineData' in p: Image.open(io.BytesIO(base64.b64decode(p['inlineData']['data']))).convert('RGB').resize(patch.size,Image.LANCZOS).save(f'REPOSE-{n+1:02d}.png')
    print('repose',n+1,flush=True)
json.dump({'box':box},open('repose_box.json','w'))
c=Image.new('RGB',(4*360,480),'white'); c.paste(patch.resize((360,480)),(0,0))
for n in range(3):
    try: c.paste(Image.open(f'REPOSE-{n+1:02d}.png').resize((360,480)),(360*(n+1),0))
    except Exception: pass
c.save('/tmp/claude-0/-home-user-ARC-REPOS/00150b4b-793a-515e-884e-50e331ae2575/scratchpad/repose.jpg')
