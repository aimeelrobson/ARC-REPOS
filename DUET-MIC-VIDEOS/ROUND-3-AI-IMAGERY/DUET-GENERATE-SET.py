import sys, json, base64, urllib.request, time, concurrent.futures as cf
B='/home/user/ARC-REPOS/DUET-MIC-VIDEOS/ROUND-3-AI-IMAGERY/'
MODEL='gemini-3-pro-image'
def img(p): return {"inline_data":{"mime_type":"image/png" if p.endswith('png') else "image/jpeg","data":base64.b64encode(open(B+p,'rb').read()).decode()}}
REFS=['PRODUCT-PHOTOS/KIT-BLUSH.png','PRODUCT-PHOTOS/REF-MIC-BLUSH-FRONT.png','PRODUCT-PHOTOS/REF-MIC-BLUSH-WINDSHIELD.png']
MIC=("PRODUCT ACCURACY IS CRITICAL. The reference images show the exact DUET microphone. Every microphone in the image must be an exact copy: "
"a small vertical blush-pink rounded-rectangle body (about 5 cm tall, thumb-sized); on top either a white rounded-square foam head or a round fluffy pink faux-fur windshield; "
"ONE large rounded-square button centred on the front; ONE tiny green LED dot above the button; the back clip's two small tabs visible poking out either side of the button. "
"The receiver (if shown) is a small flat pink rectangle with a USB-C plug on one side and one square button. "
"ABSOLUTELY NO text, logos, lettering or branding on the microphones, receiver or anywhere in the image. No extra LEDs, no screens, no cables on the mics. "
"When worn, the mic is clipped vertically to the collar or neckline, head pointing up, clearly visible and in sharp focus.")
STYLE=("Art direction: pastel maximalism, kitsch retro-whimsy, Barbiecore/coquette, editorial surrealism. Palette bubblegum pink, mint, lilac, butter yellow, tangerine, brass accents. "
"Hard flash or direct sunlight, crisp graphic shadows, saturated colour, premium high-end campaign photography, witty and chic, never cheap. No alcohol.")
JOBS={
# PEOPLE
'DUET-PEOPLE-01-BATHTUB':"Two stylish young women in their twenties, fully dressed, sit side by side in a vintage pastel-pink tiled bathtub overflowing with white foam bubbles. One wears an oversized lilac blazer with layered pearls, the other a butter-yellow cardigan and a pink claw clip. Each wears one pink DUET mic with fluffy pink windshield clipped vertically at her neckline. They laugh while filming themselves on a smartphone on a small pink tripod on the tub edge. Mint-green wall tiles, a pink rotary wall telephone with coiled cord, floating soap bubbles. Deadpan surreal humour.",
'DUET-PEOPLE-02-SOFA-PODCAST':"Two friends in matching magenta-and-pink striped pyjamas with big Peter Pan collars lounge on a pink-and-butter-yellow striped sofa recording a podcast, talking animatedly to each other. Each wears a pink DUET mic clipped vertically on her collar. A phone on a small pink tripod films them. Pink walls, a plate of pink glazed donuts and two strawberry milkshakes with striped straws on the coffee table, pom-pom slippers.",
'DUET-PEOPLE-03-GIANT-PHONE':"Editorial surrealism: two young women in Barbiecore outfits (one in a hot-pink tailored suit, one in a lilac tulle dress) interview each other while sitting on top of a giant oversized pastel-pink rotary telephone, its huge coiled cord looping across a mint studio floor. Each wears a pink DUET mic with white foam head clipped vertically at her collar. Pastel mint seamless backdrop, hard flash, long crisp shadows, absurd and chic.",
'DUET-PEOPLE-04-GRWM-VANITY':"Two friends in towel turbans (one pink, one coral) and pink-and-orange checkered bathrobes film a get-ready-with-me video at a lilac gridded tile vanity table, one mid-lipgloss with a playful pout, the other laughing. Each wears a pink DUET mic clipped vertically on her robe lapel. Phone on a mini pink tripod, heart-shaped hand mirror, claw clips, pink comb. Soft pink wall.",
# SCENES
'DUET-SCENE-01-RADIO-TILES':"Styled product still life: the pair of pink DUET mics (white foam heads) and the pink receiver plus two fluffy pink windshields arranged on a bubblegum-pink gridded ceramic tile tabletop with white grout. A retro mint-green transistor radio with brass dial, a brass twin-bell alarm clock, scattered popcorn, and a pink rotary telephone handset whose coiled cord curls around the mics. Mint and pink tiled wall. The mics are the sharp hero.",
'DUET-SCENE-02-CREATOR-FLATLAY':"Top-down flat lay on a periwinkle-blue surface: the pair of pink DUET mics with fluffy pink windshields and the pink receiver at the centre, surrounded by a pink rotary telephone with coiled cord, a lilac keyboard, pink pens, hot-pink pushpins, a mint binder clip, a phone with a pink case. Hard sunlight, crisp shadows, playful organised chaos with the mics as the clear hero.",
'DUET-SCENE-03-RETRO-TV':"Kitsch retro interior still life: the pair of pink DUET mics standing upright on a pink shelf in front of a pink-and-mint 1960s television set, next to a brass alarm clock, a cream retro toaster and a glass jar of popcorn. Pink square-tiled wall, potted snake plant. Warm hard light, saturated pastel palette. Mics in sharp focus in the foreground.",
'DUET-SCENE-04-DONUT-STACK':"Kitsch surreal still life: the two pink DUET mics with fluffy pink windshields perched on top of a tall stack of pink glazed donuts with rainbow sprinkles, on a butter-yellow and pink striped backdrop and tabletop. Hard flash, crisp shadow, playful and edible-looking. Mics sharp and hero-sized.",
# HERO (01 already exists as TEST-03)
'DUET-HERO-02-THE-COUPLE':"Minimal luxury hero shot: two pink DUET mics with fluffy pink windshields stand facing each other like a couple on a glossy lilac cylindrical plinth, against a mint-to-pale-pink gradient backdrop. Hard sunlight casting two crisp overlapping shadows. Generous negative space, gallery-object feel, romantic and witty.",
'DUET-HERO-03-BUBBLES':"Surreal hero shot: a single pink DUET mic with its fluffy pink windshield floats weightlessly in mid-air among iridescent soap bubbles, against a smooth bubblegum-pink to peach gradient sky. Soft glow, crisp detail on the mic, dreamy yet premium.",
}
EXTRA={}
def run(name):
    parts=[img(r) for r in REFS]+[{"text":MIC+"\n\nSCENE: "+JOBS[name]+"\n\n"+STYLE}]
    body={"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"4:5"}}}
    for attempt in range(4):
        req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
        try: d=json.load(urllib.request.urlopen(req,timeout=300))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,503) and attempt<3: time.sleep(20*(attempt+1)); continue
            return name,'HTTP %s %s'%(e.code,e.read().decode()[:200])
        for c in d.get('candidates',[]):
            for p in c.get('content',{}).get('parts',[]):
                if 'inlineData' in p:
                    out=B+'SET-4X5/'+name+'.jpg'; open(out,'wb').write(base64.b64decode(p['inlineData']['data'])); return name,'ok'
        return name,'NO IMAGE '+json.dumps(d)[:200]
names=sys.argv[1:] or list(JOBS)
with cf.ThreadPoolExecutor(3) as ex:
    for n,r in ex.map(run,names): print(n,r,flush=True)
