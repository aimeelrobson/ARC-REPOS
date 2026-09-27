# Edit Aimée's hero: matching pink chairs, Blush mics, restyle the right-hand model.
# Usage: python3 DUET-EDIT-PINK-CHAIRS.py RED|NOIR TAKE_NO
import sys, json, base64, urllib.request, time
B='/home/user/ARC-REPOS/DUET-MIC-VIDEOS/ROUND-3-AI-IMAGERY/'
H=B+'HERO-PINK-CHAIRS/'
MODEL='gemini-3-pro-image'
def img(p):
    return {"inline_data":{"mime_type":"image/png" if p.endswith('png') else "image/jpeg","data":base64.b64encode(open(p,'rb').read()).decode()}}
OUTFIT={
'RED':"an oversized cherry-red (#C8102E) tailored blazer with sharp padded shoulders and sleeves pushed up, worn as a mini blazer-dress over bare legs, collar open to a simple neckline, small gold hoop earrings, sleek slicked-back hair kept as it is, and red-tinted rectangular sunglasses",
'NOIR':"an oversized ink-black tailored blazer with sharp padded shoulders and sleeves pushed up, worn as a mini blazer-dress over bare legs, collar open to a simple neckline, small gold hoop earrings, sleek slicked-back hair kept as it is, and slim black rectangular sunglasses",
}
def prompt(o): return (
"Edit this photograph. Keep the composition, camera angle, lilac room, lighting, image style and texture exactly the same. Keep the brunette woman on the LEFT exactly as she is: same face, expression, hair, white sunglasses, butter-yellow jacket and skirt, pose and her pink chair — do not change her at all.\n\n"
"CHANGES:\n"
"1. The chair on the RIGHT becomes an exact twin of the left chair: the same bubblegum-pink moulded shell seat with the same shape, finish and colour. Both chairs match.\n"
"2. The blonde woman on the RIGHT keeps her face, slicked-back blonde hair, body pose (leaning back-to-back against the brunette, legs crossed) but is restyled in "+OUTFIT[o]+". Her expression becomes cool and knowing: chin slightly raised, a small closed-mouth smirk, not laughing. Effortless, too-cool, fashion-editorial attitude.\n"
"3. Microphones: BOTH microphones become the Blush colourway shown in the reference images — a pale blush-pink body with a white rounded-square foam head, one large rounded-square button on the front, one tiny green LED dot above it, and the clip's two small tabs poking out either side. The brunette keeps holding hers exactly where it is, same size, button to camera. The blonde holds hers upright between her fingers in front of her blazer at chest height, button facing camera, same size as the brunette's (about the length of a finger), sharp and clearly readable against the dark fabric.\n\n"
"ABSOLUTELY NO text, logos or lettering on the microphones or anywhere. No extra objects. Premium fashion-campaign quality.")
def run(o,n):
    parts=[img(H+'DUET-HERO-PINK-CHAIRS-SOURCE-AIMEE.jpg'),img(B+'PRODUCT-PHOTOS/REF-MIC-BLUSH-FRONT.png'),img(B+'PRODUCT-PHOTOS/KIT-BLUSH.png'),{"text":prompt(o)}]
    body={"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9","imageSize":"4K"}}}
    for a in range(4):
        req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
        try: d=json.load(urllib.request.urlopen(req,timeout=400))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,503) and a<3: time.sleep(20*(a+1)); continue
            return f'HTTP {e.code} {e.read().decode()[:300]}'
        for c in d.get('candidates',[]):
            for p in c.get('content',{}).get('parts',[]):
                if 'inlineData' in p:
                    out=f'{H}WORKING/{o}-{n}.jpg'; open(out,'wb').write(base64.b64decode(p['inlineData']['data'])); return out
        return 'NO IMAGE '+json.dumps(d)[:300]
if __name__=='__main__': print(run(sys.argv[1],sys.argv[2]))
