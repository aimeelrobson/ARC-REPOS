"""Swap the black mics in the lemon-chairs photo for Cloud (white) DUET mics. Gemini image edit, product refs attached."""
import sys,json,base64,urllib.request,time,os,concurrent.futures as cf
H=os.path.dirname(os.path.abspath(__file__)); P=os.path.join(H,'..','PRODUCT-PHOTOS')
def img(f,mt=None):
    mt=mt or ('image/png' if f.endswith('.png') else 'image/jpeg')
    return {"inline_data":{"mime_type":mt,"data":base64.b64encode(open(f,'rb').read()).decode()}}
PROMPT=("Edit the FIRST image (the photograph). The other images are product references for the DUET wireless clip-on microphone in the white 'Cloud' colourway.\n\n"
"1. Remove both small black microphones from the photograph completely, repairing skin, fingers and fabric underneath.\n"
"2. Add white Cloud DUET microphones that are exact copies of the reference: a small vertical white rounded-rectangle body with a white rounded-square foam cap on top, "
"ONE large rounded-square button centred on the front, ONE tiny green LED dot above the button, the back clip's two small tabs just visible either side of the button. No logos, no text, no extra details.\n"
"   - Brunette on the LEFT: she holds one mic pinched between her thumb and forefinger at chest height (where the black mic was), front face toward the camera so the button and green LED are visible, "
"angled slightly toward the lens. Her thumb overlaps IN FRONT of the mic body.\n"
"   - Blonde on the RIGHT: her mic is CLIPPED to the top edge of her floral top's neckline, just below her collarbone at the front of her shoulder (near her chin, high on the chest, NOT at the waist), upright, its front facing the camera. Her raised hand keeps the same natural laughing gesture near her sunglasses but is now EMPTY.\n"
"3. SCALE IS CRITICAL: each white mic must be EXACTLY THE SAME SIZE as the black microphone it replaces in the original photo (about 6.5 cm tall with cap, 1.5 cm wide): no longer than the model's index finger and about one finger wide. Tiny and dainty. If in doubt, make it smaller.\n"
"4. Integrate photographically: key light from the window on the right; matching highlights, soft contact shadows where the mic meets fingers and fabric. "
"Warm the whites slightly to sit with the skin tones, no blown-out pure white. Match the photo's grain and softness.\n"
"5. Change NOTHING else: faces, expressions, sunglasses, hair, outfits, poses, chairs, room and colour grade stay identical. Same framing and aspect ratio.")
def run(i):
    parts=[img(os.path.join(H,'POTENTIAL-HEADER-SHOT-SOURCE.jpg')),img(os.path.join(P,'REF-MIC-CLOUD-FRONT.png')),img(os.path.join(P,'KIT-CLOUD.png')),img(os.path.join(P,'REF-MIC-WORN.png')),{"text":PROMPT}]
    body={"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9","imageSize":"4K"}}}
    for a in range(4):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=300))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,503) and a<3: time.sleep(20*(a+1)); continue
            return i,'HTTP %s %s'%(e.code,e.read()[:300])
        for c in d.get('candidates',[]):
            for p in c.get('content',{}).get('parts',[]):
                if 'inlineData' in p:
                    out=os.path.join(H,f'TAKE-{i:02d}.png');open(out,'wb').write(base64.b64decode(p['inlineData']['data']));return i,'ok'
        return i,'NO IMAGE '+json.dumps(d)[:300]
if __name__=='__main__':
    ids=[int(x) for x in sys.argv[1:]] or [1,2,3]
    with cf.ThreadPoolExecutor(3) as ex:
        for i,r in ex.map(run,ids): print(i,r,flush=True)
