# Recolour the blazer on the approved Noir composition to cherry red; nothing else changes.
import sys, json, base64, urllib.request, time
H='/home/user/ARC-REPOS/DUET-MIC-VIDEOS/ROUND-3-AI-IMAGERY/HERO-PINK-CHAIRS/'
def img(p): return {"inline_data":{"mime_type":"image/jpeg","data":base64.b64encode(open(p,'rb').read()).decode()}}
P=("Edit this photograph with ONE change only: the blonde woman's black blazer-dress becomes a rich cherry-red (#C8102E) blazer-dress with the same cut, folds, padded shoulders and fit, and her black sunglasses become red-tinted rectangular sunglasses with thin gold frames. "
"Everything else stays pixel-identical: both faces, both poses, the back-to-back seating, the brunette and her butter-yellow outfit, both pink chairs, the lilac room, lighting, texture, and both pale blush-pink microphones with white foam heads in exactly the same positions and size. No text or logos.")
def run(n):
    body={"contents":[{"parts":[img(H+'WORKING/NOIR-01.jpg'),{"text":P}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9","imageSize":"4K"}}}
    for a in range(4):
        req=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
        try: d=json.load(urllib.request.urlopen(req,timeout=400))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,503) and a<3: time.sleep(20*(a+1)); continue
            return f'HTTP {e.code}'
        for c in d.get('candidates',[]):
            for p in c.get('content',{}).get('parts',[]):
                if 'inlineData' in p:
                    out=f'{H}WORKING/RED-ON-NOIR-{n}.jpg'; open(out,'wb').write(base64.b64decode(p['inlineData']['data'])); return out
        return 'NO IMAGE'
print(run(sys.argv[1]))
