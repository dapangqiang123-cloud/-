import json,subprocess,uuid,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R/'制作文件/jobs.json';pid='721c8a46-7d95-4d63-b843-f04857486e51'
s=json.loads(S.read_text()) if S.exists() else {'projectId':pid,'budget':1000,'reserved':0,'jobs':{}}
def save():S.write_text(json.dumps(s,ensure_ascii=False,indent=2))
def cli(*a):
 p=subprocess.run(['dreamina-canvas',*map(str,a),'--project-id',pid],capture_output=True,text=True)
 try:d=json.loads(p.stdout)
 except:raise RuntimeError(p.stderr[:300])
 if not d.get('ok'):raise RuntimeError(json.dumps(d,ensure_ascii=False))
 return d
P={
'mountain': 'Editorial photographic collage source asset. A majestic rugged limestone mountain massif and layered rolling hills with Mediterranean olive-green grass, tiny dark pine trees, warm taupe stone and a few golden grassy slopes. Straight-on landscape view, broad panoramic skyline at varying heights, sharp realistic photographic rock detail, like a carefully hand-cut National Geographic magazine photograph. Entire mountains fully inside the canvas with generous empty margins. Isolated on perfectly pure white #FFFFFF background, no blue sky, no clouds, no frame, no text, no paper border, no drop shadow. The mountain occupies the lower 70 percent. Natural sunny warm light, muted elegant earthy palette. NOT an illustration, NOT a miniature toy, NOT CGI. High-end editorial art direction, fine restrained photographic grain.',
'forest': 'Single photographic cutout asset: a broad rolling forest-covered hill, dense olive-green and sage-green trees, rocky taupe outcrops, one tiny meandering pathway through golden meadow. Eye-level view from distance, lower foreground evergreen branch on right. Wide low silhouette, hill fully visible within frame. Isolated on pure white #FFFFFF background, generous white margins, no sky, no text, no border, no shadow. Real photographic detail, sunny warm late-afternoon natural light, sophisticated muted earthy colors, magazine cutout, crisp tree foliage. NOT watercolor, NOT illustration, NOT 3D render.',
'room': 'Luxury architectural editorial photograph, warm modern Chinese home, 16:9 horizontal composition, eye-level wide angle 28mm. Cream plaster walls, pale oak, rounded ivory linen sofa low in the frame, sculptural walnut coffee table, one art book and ceramic tea cup, floor lamp, olive tree, beautiful full height windows with sheer linen curtains to the RIGHT, subtle long narrow integrated ceiling ventilation slot above the window on the upper wall. Daylight and soft sun shadows from right. Calm cozy inhabited room but no people. Restrained beige champagne warm gray sage palette, very high detail upholstery and architecture. Main sofa near bottom center, clean large wall upper left for later graphics. Beautiful believable high-end interior photography, natural optics, no surreal shapes, no letters, no logos, no frame, no visible appliances, no floating objects, no busy decoration.',
'chair': 'One isolated full-body photographic lifestyle cutout for sophisticated mixed-media editorial animation. A stylish Chinese woman around 30 with natural realistic face, wearing a cream knit sweater and taupe trousers, seated comfortably sideways in a rounded warm ivory boucle lounge chair, calmly reading a small book. Bare feet resting on a matching low ottoman. Slim dark bronze floor reading lamp to her right. Entire woman chair ottoman and lamp fully visible, generous margins on all sides. Pure white #FFFFFF seamless background, no floor line, no shadows outside subject. Natural soft sunlight, authentic lived-in candid expression, premium furniture editorial photograph, sharp details, sophisticated beige and warm brown palette, no lettering or watermarks, no extra fingers, no plastic skin.',
'leaf': 'A single elegant large ginkgo leaf, pale champagne gold with olive green base, clearly visible fine veins, delicate fan shape, slender curved stem, side-lit natural macro photograph, isolated in the center on pure white #FFFFFF background. Whole leaf visible, plenty of white space, no other objects, no shadow, no text, no illustration. Luxury botanical editorial photography.'}
cmd=sys.argv[1]
if cmd=='create':
 for key,prompt in P.items():
  if key in s['jobs']:continue
  d=cli('node','create','image','--title',key,'--mode','t2i','--model','seedream_5.0_pro','--ratio','16:9' if key in ('mountain','forest','room') else '1:1','--resolution','4K','--count',1,'--prompt',prompt)
  s['jobs'][key]={'nodeId':d['data']['node']['nodeId'],'submitId':str(uuid.uuid4()),'prompt':prompt};save()
  print('CREATED',key,flush=True)
 for key,j in s['jobs'].items():
  if j.get('submitted'):continue
  d=cli('node','quote','--node-id',j['nodeId']);cost=d['data']['totalMaxCredits'];assert s['reserved']+cost<=1000
  print('QUOTE',key,cost,flush=True)
  conf=cli('node','confirm','--node-id',j['nodeId'],'--credit-ceiling',cost)
  j.update(reserved=cost,submitted='submitting');s['reserved']+=cost;save()
  d=cli('node','run','--node-id',j['nodeId'],'--submit-id',j['submitId'],'--credit-token',conf['data']['creditConfirmationToken'])
  j['submitted']='accepted';j['requestId']=d.get('meta',{}).get('requestId');save();print('ACCEPTED',key,flush=True)
elif cmd=='status':
 for key,j in s['jobs'].items():
  d=cli('operation','status',j['submitId']);j['status']=d['data'];save();print(key,d['data']['state'],flush=True)
  for res in d['data'].get('resources',[]):
   if res['state']=='succeeded' and not j.get('downloaded'):
    out=R/'素材'/(key+('.mp3' if j.get('kind')=='audio' else '.png'));r=cli('resource','download',res['resourceId'],'--output',out);j['downloaded']=str(out);j['resourceId']=res['resourceId'];save();print('DOWNLOADED',key,flush=True)
