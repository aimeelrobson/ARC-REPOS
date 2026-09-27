"""Swap each Blush mic for a true-size Cloud mic (6.5 x 1.5 cm) with a crisp drop shadow. Gemini edits square patches only.
Usage: python3 DUET-TRUE-SIZE-MICS.py L|R PLAIN|MINT TAKE"""
import sys, json, base64, urllib.request, io, time
from PIL import Image
H='/home/user/ARC-REPOS/DUET-MIC-VIDEOS/ROUND-3-AI-IMAGERY/'
BOX={'L':(1850,1250,2750,2150),'R':(3030,1150,3930,2050)}
WHO={'L':"The brunette's hand presses the microphone flat against her butter-yellow jacket sleeve, thumb/finger on the button.",
     'R':"The woman's hand holds the microphone upright in front of her red blazer, fingers curled around its lower body."}
def enc(im):
    b=io.BytesIO(); im.save(b,'PNG'); return {"inline_data":{"mime_type":"image/png","data":base64.b64encode(b.getvalue()).decode()}}
side,var,n=sys.argv[1],sys.argv[2],sys.argv[3]
M=Image.open(H+'HERO-PINK-CHAIRS/DUET-HERO-PINK-CHAIRS-RED-MASTER.png').convert('RGB')
patch=M.crop(BOX[side])
P=("Edit the FIRST image, a close crop of a fashion photograph. "+WHO[side]+" The pink microphone in it is far TOO BIG.\n"
"Replace it with the white DUET microphone shown in the SECOND and THIRD images, at TRUE SIZE: the real mic is 6.5 cm tall including its foam cap and 1.5 cm wide. "
"HARD SIZE LIMIT: in this crop the new microphone (cap + body together) must be only about 20% of the image height (roughly 1/5) and its body about 5% of the image width, i.e. HALF the size of the current pink one. Its whole length equals her index finger. It looks small and precious, mostly wrapped by her fingers. "
"Same place, same grip, same angle, front facing camera. Design exactly as the references: white rounded-square foam cap, white body, one large rounded-square button, one tiny green LED dot above it, two small clip tabs either side. "
"Where the old, larger microphone was, restore the fabric and hand naturally (matching folds, texture and colour). Re-pose the fingers naturally around the smaller mic. "
"Make the white mic the sharpest, brightest point of the crop: add a crisp, soft-edged drop shadow on the fabric behind it, offset slightly down and to the right, as if lit by a direct fashion flash, so it separates clearly from the background. "
+("Paint her fingernails a glossy mint-teal (#7FD1C0) so the colour frames the white mic. " if var=='MINT' else "")+
"Change nothing else: keep skin, fabric colour, lighting, texture and painterly style identical. No text, no logos.")
body={"contents":[{"parts":[enc(patch),enc(Image.open(H+'PRODUCT-PHOTOS/REF-MIC-CLOUD-FRONT.png').convert('RGB')),enc(Image.open(H+'PRODUCT-PHOTOS/REF-MIC-CLOUD-SET.png').convert('RGB')),{"text":P}]}],
      "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1","imageSize":"2K"}}}
for a in range(4):
    try: d=json.load(urllib.request.urlopen(urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=400)); break
    except urllib.error.HTTPError as e:
        if e.code in (429,500,502,503,504) and a<3: time.sleep(20*(a+1)); continue
        raise
for c in d.get('candidates',[]):
    for p in c.get('content',{}).get('parts',[]):
        if 'inlineData' in p:
            Image.open(io.BytesIO(base64.b64decode(p['inlineData']['data']))).convert('RGB').resize(patch.size,Image.LANCZOS).save(f'WORKING/MIC-{side}-{var}-{n}.png'); print('ok',side,var,n); sys.exit()
print('NO IMAGE',side,var,n)
