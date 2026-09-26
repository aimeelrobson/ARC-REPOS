import sys, json, base64, urllib.request, pathlib, concurrent.futures as cf
B='/home/user/ARC-REPOS/DUET-MIC-VIDEOS/ROUND-3-AI-IMAGERY/'
MODEL='gemini-3-pro-image'
PRODUCT=("The reference photo shows the exact DUET product: a blush-pink wireless clip-on lavalier microphone kit "
 "(two thumb-sized pink rounded-rectangle transmitters with a white rounded-square foam head, a large square front button, a tiny green LED, a back clip; "
 "a small matching pink USB-C receiver; fluffy pink faux-fur windshields). Reproduce the product faithfully: same shape, proportions, colour and details. No visible logos or text on the product.")
STYLE=("Art direction: pastel maximalism, kitsch retro-whimsy, Barbiecore/coquette, editorial surrealism. Palette bubblegum pink, mint, lilac, butter yellow, tangerine, brass accents. "
 "Hard flash / direct sunlight, crisp graphic shadows, saturated, premium high-end campaign photography, witty and chic, never cheap. No alcohol. No text or watermarks.")
JOBS={
'TEST-01-PEOPLE-BATHTUB':"Editorial fashion photograph: two stylish young women in their twenties, fully dressed, sit side by side in a vintage pastel-pink tiled bathtub overflowing with white foam bubbles. One wears an oversized lilac blazer with layered pearls, the other a butter-yellow knit and a pink claw clip. Each has one of the pink DUET microphones clearly visible clipped to her collar, with its fluffy pink windshield. They laugh while filming themselves on a smartphone on a small pink tripod balanced on the tub edge. Mint-green wall tiles, a pink rotary wall telephone with coiled cord, floating soap bubbles. Deadpan surreal humour.",
'TEST-02-PRODUCT-IN-SCENE':"Styled product still life: the pair of pink DUET microphones and the pink receiver, plus two fluffy windshields, arranged on a bubblegum-pink gridded ceramic tile tabletop with white grout. Styled with a retro mint-green transistor radio with brass dial, a brass twin-bell alarm clock, scattered popcorn, and a pink rotary telephone handset whose coiled cord curls playfully around the microphones. Mint and pink tiled wall behind. The microphones are the sharp, hero focus.",
'TEST-03-PRODUCT-HERO':"Minimal luxury hero product photograph: a single pink DUET microphone with its fluffy pink windshield standing upright on top of a sculptural wavy tangerine-orange plinth. Pink-and-orange checkerboard floor, soft pink-to-tangerine gradient backdrop, one slice of pink grapefruit at the base. Hard sunlight casting a crisp long shadow. Generous negative space, surreal gallery-object feel.",
}
ref=base64.b64encode(open(B+'PRODUCT-PHOTOS/KIT-BLUSH.png','rb').read()).decode()
def run(name,prompt):
    body={"contents":[{"parts":[{"inline_data":{"mime_type":"image/png","data":ref}},{"text":PRODUCT+"\n\nScene: "+prompt+"\n\n"+STYLE}]}],
          "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"4:5"}}}
    req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
    try: d=json.load(urllib.request.urlopen(req,timeout=300))
    except urllib.error.HTTPError as e: return name,'HTTP '+str(e.code)+' '+e.read().decode()[:300]
    for c in d.get('candidates',[]):
        for p in c.get('content',{}).get('parts',[]):
            if 'inlineData' in p:
                ext='png' if 'png' in p['inlineData'].get('mimeType','') else 'jpg'
                out=B+f'TESTS/{name}.{ext}'; open(out,'wb').write(base64.b64decode(p['inlineData']['data'])); return name,out
    return name,'NO IMAGE '+json.dumps(d)[:300]
names=sys.argv[1:] or list(JOBS)
with cf.ThreadPoolExecutor(3) as ex:
    for n,r in ex.map(lambda n: run(n,JOBS[n]), names): print(n,'->',r)
