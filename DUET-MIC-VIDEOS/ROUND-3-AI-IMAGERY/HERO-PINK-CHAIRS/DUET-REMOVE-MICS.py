"""Step 1: remove each oversized mic from its patch, restoring fabric; fingers left in a light pinch. Usage: L|R TAKE"""
import sys, json, base64, urllib.request, io, time
from PIL import Image
H='/home/user/ARC-REPOS/DUET-MIC-VIDEOS/ROUND-3-AI-IMAGERY/HERO-PINK-CHAIRS/'
BOX={'L':(1850,1250,2750,2150),'R':(3030,1150,3930,2050)}
side,n=sys.argv[1],sys.argv[2]
patch=Image.open(H+'DUET-HERO-PINK-CHAIRS-RED-MASTER.png').convert('RGB').crop(BOX[side])
b=io.BytesIO(); patch.save(b,'PNG')
P=("Edit this close crop of a fashion photograph: REMOVE the pink-and-white microphone completely. "
"Restore what was behind it naturally: continue the fabric folds, texture and colour"+(" of the butter-yellow jacket" if side=='L' else " of the red blazer")+". "
"Keep her hand in the same place and size, with the thumb and index finger lightly pinched together as if holding a tiny object (1.5 cm wide) between the fingertips. "
"Change nothing else: same skin, same lighting, same painterly texture and colours. No new objects, no text.")
body={"contents":[{"parts":[{"inline_data":{"mime_type":"image/png","data":base64.b64encode(b.getvalue()).decode()}},{"text":P}]}],
      "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1","imageSize":"2K"}}}
for a in range(5):
    try: d=json.load(urllib.request.urlopen(urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=400)); break
    except urllib.error.HTTPError as e:
        if e.code in (429,500,502,503,504) and a<4: time.sleep(20*(a+1)); continue
        raise
for c in d.get('candidates',[]):
    for p in c.get('content',{}).get('parts',[]):
        if 'inlineData' in p:
            Image.open(io.BytesIO(base64.b64decode(p['inlineData']['data']))).convert('RGB').resize(patch.size,Image.LANCZOS).save(f'{H}WORKING/NOMIC-{side}-{n}.png'); print('ok',side,n); sys.exit()
print('NO IMAGE',side,n)
