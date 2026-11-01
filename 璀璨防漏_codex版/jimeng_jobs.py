import subprocess,json,uuid,csv,datetime,sys
from pathlib import Path
R=Path(__file__).resolve().parent
PID='62aee2d2-30d8-40db-982a-008c616b6d86'
STATE=R/'logs/jimeng_state.json'
st=json.loads(STATE.read_text()) if STATE.exists() else {'projectId':PID,'jobs':{},'committed':0}
def save():STATE.write_text(json.dumps(st,ensure_ascii=False,indent=2));STATE.chmod(0o600)
def call(*args):
 p=subprocess.run(['dreamina-canvas',*map(str,args)],capture_output=True,text=True)
 try:d=json.loads(p.stdout)
 except:raise RuntimeError(p.stderr[:300])
 if not d.get('ok'):raise RuntimeError(json.dumps(d,ensure_ascii=False))
 return d
job=sys.argv[1]
if job=='house':
 j=st['jobs'].setdefault(job,{'nodeId':'node_pzwfpxgvse','submitId':'1075ea73-a9cf-4ff7-a935-86a165de5f89','seconds':6})
elif job in ('cup','renovation'):
 duration={'cup':4,'renovation':6}[job]
 prompts={'cup':'4秒，单镜头90mm微距，轻微缓推，保持玻璃杯原形。真实冷凝小水珠在杯壁汇聚，一颗较大水珠沿玻璃外侧缓慢向下滑，冰块静止。温暖自然侧光，浅景深，光学真实，无凭空大量流水。无文字、Logo、水印、字幕、型号、畸形、闪烁、穿模、杯体变形、快速运镜。','renovation':'6秒，单镜头，中广景，保持首帧室内建筑和人物身份。极慢横向滑轨，业主与设计师先低头看浅色木石样板，再自然抬头看吊顶风口，人物幅度小，神态认真不夸张。明亮暖白自然光，淡暖木色。侧面横向线性风口完全保持，不增加机器。上20%下25%不放关键动作。无文字、Logo、水印、字幕、型号、畸形手、额外手指、闪烁、穿模、建筑变形、室内室外机、壁挂机、柜机。'}
 if job not in st['jobs']:
  st['jobs'][job]={'resourceId':str(uuid.uuid4()),'uploadDone':False,'submitId':str(uuid.uuid4()),'seconds':duration};save()
 j=st['jobs'][job]
 if not j['uploadDone']:
  call('resource','upload','--project-id',PID,'--file',R/'assets'/f'{job}.png','--resource-id',j['resourceId'],'--import-kind','external_generated');j['uploadDone']=True;save()
 if 'imageNodeId' not in j:
  d=call('node','create','image','--project-id',PID,'--title',job+'首帧','--resource-id',j['resourceId'],'--import-kind','external_generated');j['imageNodeId']=d['data']['node']['nodeId'];save()
 if 'nodeId' not in j:
  d=call('node','create','video','--project-id',PID,'--title',job,'--mode','first_last_frame','--model','seedance_2.0_fast_vip','--ratio','9:16','--resolution','720p','--duration',duration,'--ref','node:'+j['imageNodeId'],'--prompt',prompts[job]);j['nodeId']=d['data']['node']['nodeId'];j['prompt']=prompts[job];save()
else:raise Exception('unknown')
if not j.get('submitted'):
 q=call('node','quote','--project-id',PID,'--node-id',j['nodeId']);print('QUOTE',json.dumps(q,ensure_ascii=False),flush=True)
 ceiling=j['seconds']*6
 assert st['committed']+ceiling<=1000
 conf=call('node','confirm','--project-id',PID,'--node-id',j['nodeId'],'--credit-ceiling',ceiling)
 def token(o):
  if isinstance(o,dict):
   for k,v in o.items():
    if k=='creditConfirmationToken':return v
    t=token(v)
    if t:return t
  elif isinstance(o,list):
   for v in o:
    t=token(v)
    if t:return t
 t=token(conf)
 assert t
 j['reserved']=ceiling;st['committed']+=ceiling;j['submitted']='submitting';save()
 d=call('node','run','--project-id',PID,'--node-id',j['nodeId'],'--submit-id',j['submitId'],'--credit-token',t)
 j['submitted']='accepted';save()
 with (R/'logs/jimeng_ledger.csv').open('a') as f:csv.writer(f).writerow([datetime.datetime.now().isoformat(),job,j['seconds'],ceiling,st['committed'],'待生成核验',j['submitId']])
 print('ACCEPTED',json.dumps(d,ensure_ascii=False),flush=True)
else:print('already submitted',j['submitId'])
