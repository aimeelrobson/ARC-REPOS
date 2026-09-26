import sys,json,base64,urllib.request,time,glob,os,concurrent.futures as cf
B='/home/user/ARC-REPOS/DUET-MIC-VIDEOS/ROUND-3-AI-IMAGERY/'
P=("Recompose this exact photograph as a tall 9:16 vertical image for Instagram Stories by naturally extending the scene above and below (more backdrop, floor, tiles or set). "
"Keep every existing element identical: same people, faces, outfits, poses, props, lighting, colours and especially the microphones exactly as they are. "
"Do not add any text, logos or new microphones. Leave calm space near the top and bottom for captions.")
def run(f):
    name=os.path.basename(f)
    body={"contents":[{"parts":[{"inline_data":{"mime_type":"image/jpeg","data":base64.b64encode(open(f,'rb').read()).decode()}},{"text":P}]}],
          "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"9:16"}}}
    for a in range(4):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=300))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,503) and a<3: time.sleep(20*(a+1)); continue
            return name,'HTTP %s'%e.code
        for c in d.get('candidates',[]):
            for p in c.get('content',{}).get('parts',[]):
                if 'inlineData' in p: open(B+'SET-9X16/'+name.replace('.jpg','-STORY.jpg'),'wb').write(base64.b64decode(p['inlineData']['data'])); return name,'ok'
        return name,'NO IMAGE'
fs=sys.argv[1:] or sorted(glob.glob(B+'SET-4X5/*.jpg'))
with cf.ThreadPoolExecutor(3) as ex:
    for n,r in ex.map(run,fs): print(n,r,flush=True)
