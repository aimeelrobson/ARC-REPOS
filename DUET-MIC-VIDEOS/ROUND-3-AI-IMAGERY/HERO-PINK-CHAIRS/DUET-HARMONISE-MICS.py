"""Step 3: make the placed mic photographic and wrap the fingers around it, KEEPING its size. Usage: L|R TRUE|HERO PLAIN|MINT"""
import sys, json, base64, urllib.request, io, time
from PIL import Image
H='/home/user/ARC-REPOS/DUET-MIC-VIDEOS/ROUND-3-AI-IMAGERY/'
side,tag,var=sys.argv[1:4]
src=Image.open(H+f'HERO-PINK-CHAIRS/WORKING/PLACED-{side}-{tag}.png').convert('RGB')
def enc(im):
    b=io.BytesIO(); im.save(b,'PNG'); return {"inline_data":{"mime_type":"image/png","data":base64.b64encode(b.getvalue()).decode()}}
GRIP={'L':"her index fingertip rests on the mic's front button and her thumb supports it from the side, pressing it lightly against her jacket sleeve",
      'R':"her thumb and index finger pinch its lower body naturally, the fingertips slightly overlapping the body, like holding a lipstick"}
P=("This close crop of a fashion photograph has a small white wireless microphone that was pasted in. Make it look genuinely photographed in this scene. "
"CRITICAL: the microphone must cover exactly the same pixels as now — keep its EXACT size, position and angle — do not enlarge or shrink it. Keep its design exactly as the second image: white rounded-square foam cap, white body, one rounded-square button, one tiny green LED dot, two small clip tabs. "
"Adjust only her fingers so "+GRIP[side]+". Add subtle 3D shading and a soft highlight (no sparkles, no stars) so the white mic is the brightest, crispest point, and keep a soft flash drop shadow on the fabric behind it, offset down-right. "
+("Paint her fingernails a glossy mint-teal (#7FD1C0). " if var=='MINT' else "")+
"Change nothing else: fabric, skin, colours, lighting and painterly texture stay identical. No text, no logos.")
body={"contents":[{"parts":[enc(src),enc(Image.open(H+'PRODUCT-PHOTOS/REF-MIC-CLOUD-FRONT.png').convert('RGB')),{"text":P}]}],
      "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1","imageSize":"2K"}}}
for a in range(5):
    try: d=json.load(urllib.request.urlopen(urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=400)); break
    except urllib.error.HTTPError as e:
        if e.code in (429,500,502,503,504) and a<4: time.sleep(20*(a+1)); continue
        raise
for c in d.get('candidates',[]):
    for p in c.get('content',{}).get('parts',[]):
        if 'inlineData' in p:
            Image.open(io.BytesIO(base64.b64decode(p['inlineData']['data']))).convert('RGB').resize(src.size,Image.LANCZOS).save(H+f'HERO-PINK-CHAIRS/WORKING/FINAL-{side}-{tag}-{var}{sys.argv[4] if len(sys.argv)>4 else ""}.png'); print('ok',side,tag,var); sys.exit()
print('NO IMAGE',side,tag,var)
