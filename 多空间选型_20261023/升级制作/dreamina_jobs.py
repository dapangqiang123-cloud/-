import json,subprocess,sys,uuid
from pathlib import Path
base=Path(__file__).parent/'即梦记录';statepath=base/'状态.json';state=json.loads(statepath.read_text());pid=state['projectId']
def save():statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2))
def call(args):
 p=subprocess.run(['dreamina-canvas',*args,'--project-id',pid],capture_output=True,text=True)
 raw=p.stdout.strip() or p.stderr.strip()
 try:r=json.loads(raw)
 except:raise RuntimeError('CLI未返回JSON，停止，不自动重试')
 if not r.get('ok'):print(json.dumps(r,ensure_ascii=False));raise RuntimeError('调用失败，停止，不自动重试')
 return r
plans=[
{'key':'A01','title':'A01｜客餐厅长距离送风｜仅一次','type':'video','mode':'first_last_frame','duration':9,'ref':'node_sx95dhrd71','prompt':'高级家电品牌科普广告的连续镜头，9秒，9:16竖屏。严格保持首帧照片中真实客餐厅的格局、家具、墙面、木质沙发、窗外景色与天花风口位置，不改变建筑结构，不新增设备、人物或文字。0–2秒摄影机沿客餐厅中轴平稳前移，镜头轻轻抬向天花上的黑色细长空调送风口；2–7秒从真实风口产生少量极细、半透明的柔白气流轨迹，沿天花平稳向远端餐桌方向延伸，再柔和向下散开，表现风的输送与覆盖，流线有持续向前的运动，不是固定发光线，不是烟雾；7–9秒摄影机减速，完整呈现客餐厅，气流保持运动。物理可信，细腻自然摄影光线、真实木材石材，国际高端家电广告质感。气流只是轻量科普可视化，房间始终清晰可见。绝对不要蓝色激光、霓虹、界面、字幕、数字、logo、卡通、房间变形、切镜。'},
{'key':'A02','title':'A02｜多房间系统覆盖·空间示意｜仅一次','type':'video','mode':'t2v','duration':9,'prompt':'9秒9:16竖屏，高端家电品牌的建筑可视化广告，电影级真实材质、精细光线。一个整体的现代暖木公寓剖切模型，客餐厅、主卧、儿童房、书房可见，木材、米白织物、浅色石材，细节精致而克制，模型填满竖幅构图，绝不是图表UI。0–2秒镜头沿公寓外墙缓慢升高，屋顶像建筑展示模型一样整体向上隐去，露出各房间。2–7秒摄影机做非常小幅的环绕，同时沿天花隐蔽管道，一股细腻柔白流动示意逐步分支到四个房间的窄条风口，四处都有轻柔空气流动，表现系统覆盖；7–9秒摄影机稳定在优雅的三分之四俯视角，房间光线温暖，气流继续流动。纯粹建筑原理示意，不出现任何可识别品牌或机械内部结构。无文字、无数字、无标注、无logo、无边框、无任何UI、无卡通、无水管喷水、无大块发光色带。浅暖灰真实摄影棚背景、柔和环境阴影、产品电影品质。'},
{'key':'A03','title':'A03｜微距空气过滤·概念示意｜仅一次','type':'video','mode':'t2v','duration':9,'prompt':'9秒9:16竖屏，国际高级家电品牌的微距科普广告，精细真实CG摄影，微距光学景深。画面是一片洁白的折叠式空气过滤材料，纸纤维纹理细密真实，连续整齐的折叠褶皱形成有设计感的曲面，背景深暖灰，柔和侧逆光。0–3秒镜头沿过滤材料的褶皱极慢掠过，逐渐看见空气中少量细小浅金灰尘颗粒向滤材流动；3–7秒镜头靠近纤维网的一个局部，粒径不同的尘粒被纤维拦截停留，细微柔白气流从纤维间隙继续穿过到另一侧，表现过滤因果；7–9秒摄影机顺着干净气流略微向前，亮部柔和，留下清透的呼吸感。仅为过滤概念示意，不出现真实设备、不展示化学反应、不显示除醛除菌、不承诺完全过滤。无文字、数字、logo、UI、箭头、霓虹、彩色光球、夸张激光、烟雾；清晰细节，高级自然材质。'},
{'key':'M01','title':'M01｜家的空气答案·温暖科技器乐84秒','type':'audio','mode':'music','duration':84,'prompt':'84秒纯器乐，高端中央空调品牌科普广告配乐。温暖、理性、现代、有呼吸感，约96BPM，轻柔电钢琴、细腻拨弦、圆润低音和克制的轻打击乐，低调电子空气质感。开头清晰简短，5秒起稳定流动节奏，每20秒有轻微层次变化支撑四个章节，最后6秒自然收束并留尾音。音色精致不过亮，为中文女声配音留出空间；不要人声、歌词、口哨、鸟叫、风声或其他拟音，不要史诗弦乐，不要大鼓冲击，不要舞曲高潮。'}]
action=sys.argv[1]
if action=='drafts':
 for plan in plans:
  key=plan['key']
  if key in state['items']:continue
  state['items'][key]={**plan,'submitId':str(uuid.uuid4()),'generationCount':0,'phase':'planned'};save()
  args=['node','create',plan['type'],'--title',plan['title'],'--mode',plan['mode'],'--prompt',plan['prompt'],'--duration',str(plan['duration'])]
  if plan['type']=='video':args+=['--model','seedance_2.0_fast_vip','--resolution','720p','--ratio','9:16','--count','1']
  else:args+=['--model','seed_music_1.0']
  if 'ref' in plan:args+=['--ref','node:'+plan['ref']]
  r=call(args);node=r['data']['node'];state['items'][key].update(nodeId=node['nodeId'],phase='saved',upstreamNodeIds=node['upstreamNodeIds'],requestId=r.get('meta',{}).get('requestId'));save()
  (base/(key+'_保存.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(key,node['nodeId'],node['upstreamNodeIds'],flush=True)
elif action=='quote':
 args=['node','quote']
 for item in state['items'].values():args+=['--node-id',item['nodeId']]
 r=call(args);(base/'报价.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False))
elif action=='run':
 quote=json.loads((base/'报价.json').read_text())['data'];total=quote['totalMaxCredits']
 assert total+state['committed']<=600,'超过总上限，停止'
 assert all('maxCredits' in x and not x.get('error') for x in quote['items']),'报价不完整'
 ids=[];subs=[]
 for item in state['items'].values():
  assert item['generationCount']==0 and item['phase']=='saved','禁止重复生成'
  ids+=['--node-id',item['nodeId']];subs+=['--submit-id',item['submitId']]
 conf=call(['node','confirm',*ids,'--credit-ceiling',str(total)])['data'];token=conf['creditConfirmationToken']
 for item in state['items'].values():
  item['phase']='submitting';item['generationCount']=1;item['authorizedCreditCeiling']=next(q['maxCredits'] for q in quote['items'] if q['nodeId']==item['nodeId'])
 state['committed']+=total;save()
 r=call(['node','run',*ids,*subs,'--credit-token',token]);del token
 (base/'提交结果.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
 for x in r['data']['items']:
  item=next(v for v in state['items'].values() if v['nodeId']==x['nodeId']);item.update(phase=x['state'],operationRef=x['submitId'])
 save();print(json.dumps(r,ensure_ascii=False))
elif action=='status':
 for key,item in state['items'].items():
  if item['generationCount']!=1:continue
  r=call(['operation','status',item['submitId']]);(base/(key+'_状态.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(key,json.dumps(r,ensure_ascii=False),flush=True)
