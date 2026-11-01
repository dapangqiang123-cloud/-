import json,subprocess,uuid,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R/'制作文件/jobs.json';pid='8d9cc701-cc72-496d-9246-9702773e5522'
s=json.loads(S.read_text()) if S.exists() else {'projectId':pid,'budget':1000,'reserved':0,'jobs':{}}
def save():S.write_text(json.dumps(s,ensure_ascii=False,indent=2))
def cli(*a):
 p=subprocess.run(['dreamina-canvas',*map(str,a),'--project-id',pid],capture_output=True,text=True)
 try:d=json.loads(p.stdout)
 except:raise RuntimeError(p.stderr[:300])
 if not d.get('ok'):raise RuntimeError(json.dumps(d,ensure_ascii=False))
 return d
P={'room': 'A single freestanding cutaway living room photographed straight-on with slight elevated view, like an exquisite real architectural physical scale model. Entire room box with thick cream ceiling slab and left and right side walls and pale oak floor fully visible, generous pure white #FFFFFF background around all sides. Room interior is photoreal high-end warm minimalist home: ivory curved sofa, walnut oval coffee table, small art book, bronze floor lamp, sheer curtain at right closed window, no view through windows. Long narrow black HVAC ventilation slot integrated at the upper back wall just below the ceiling. One coherent simple rectangular room, beautiful realistic material texture and soft sunlight. A crisp photographic magazine cutout, not cartoon illustration. No plants, no nature, no mountains, no human, no text, no labels, no arrows, no diagrams, no appliances elsewhere. Centered square architectural object with complete silhouette, no shadow on white background.', 'hand': 'Isolated photographic cutout of one realistic elegant adult female right hand and forearm, index finger extended pointing horizontally to the left, other fingers naturally curled, palm slightly down. Forearm enters from right edge, beige knit sweater cuff. Warm light skin, natural fingernails without polish, anatomically correct five fingers, sharp photographic details. Pure white #FFFFFF background, no shadow outside the hand, no object, no text. Side-on view for high-end editorial collage, whole index fingertip and wrist fully visible, warm soft lighting, generous white margins above and below.'}
cmd=sys.argv[1]
if cmd=='create':
 for key,prompt in P.items():
  if key in s['jobs']:continue
  d=cli('node','create','image','--title',key,'--mode','t2i','--model','seedream_5.0_pro','--ratio','1:1' if key=='room' else '16:9','--resolution','4K','--count',1,'--prompt',prompt)
  s['jobs'][key]={'nodeId':d['data']['node']['nodeId'],'submitId':str(uuid.uuid4()),'prompt':prompt};save()
  print('CREATED',key,flush=True)
 for key,j in s['jobs'].items():
  if j.get('submitted'):continue
  d=cli('node','quote','--node-id',j['nodeId']);cost=d['data']['totalMaxCredits'];assert s['reserved']+cost<=928
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
