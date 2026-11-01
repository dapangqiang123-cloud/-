import json,subprocess,uuid,sys
from pathlib import Path
base=Path(__file__).parent; sp=base/'即梦记录/状态.json';s=json.loads(sp.read_text());pid=s['projectId']
def save():sp.write_text(json.dumps(s,ensure_ascii=False,indent=2))
def call(args):
 p=subprocess.run(['dreamina-canvas',*args,'--project-id',pid],capture_output=True,text=True);r=json.loads(p.stdout.strip() or p.stderr.strip())
 if not r.get('ok'):print(json.dumps(r,ensure_ascii=False));raise RuntimeError('停止，不自动重试')
 return r
products=[('P01','C2艺境单风扇','c2.png','咖色单风扇空调室外机，正面只能有一个圆形黑色金边风扇'),('P02','C3知境双风扇','c3.jpg','咖色双风扇空调室外机，正面两个圆形黑色金边风扇上下排列'),('P03','C3D白色双风扇多联机','c3d.png','白色双风扇空调室外机，正面两个圆形黑色金边风扇上下排列'),('P04','Mini新风','mini.png','扁平的黑色长方形吊顶式新风主机，四个圆形管道接口，两侧各两个，绝不是落地式净化器')]
action=sys.argv[1]
if action=='drafts':
 for key,title,fn,desc in products:
  if key in s['items']:continue
  item={'key':key,'title':title,'type':'video','generationCount':0,'phase':'planned','uploadId':str(uuid.uuid4()),'imageSubmitId':str(uuid.uuid4()),'submitId':str(uuid.uuid4()),'duration':7,'sourceImage':str((base.parent/'完整视频工程/assets'/fn).resolve())};s['items'][key]=item;save()
  call(['resource','upload','--resource-id',item['uploadId'],'--file',item['sourceImage'],'--type','image','--name',title+'原始产品图'])
  r=call(['node','create','image','--title',title+'｜产品静态参考','--resource-id',item['uploadId'],'--import-kind','local_upload','--submit-id',item['imageSubmitId']]);item['referenceNodeId']=r['data']['node']['nodeId'];save()
  if key!='P04':
   prompt=f'7秒9:16竖屏，璀璨高端中央空调产品广告英雄镜头。参考图片中的{desc}，必须完全保持参考产品的颜色、风扇数量、金属面板比例、格栅结构、金色圆心、右上logo和各项细节，不添加屏幕或按钮。机器放在室外现代建筑的浅米色石材平台上，背景为有精细肌理的暖灰外墙、窄条深木格栅与一小处虚化的绿色植被，下午自然侧光，优雅的真实接触阴影，绝不放在室内客厅。0–2秒为产品金色风扇圆心和细密黑色格栅的质感近景，细腻掠射光从边缘经过；2–6秒摄影机平滑向后并略向右移动，逐渐显露整台准确的产品；6–7秒保持完整产品三分之四视角，让光影继续自然变化。广告级摄影，真实材质，结构稳定，产品不能变形，格栅不能旋转，机器本体静止。无新增文字、数字、字幕、UI或科幻光效。'
  else:
   prompt=f'7秒9:16竖屏，高级家电品牌产品广告。严格复现参考图中的{desc}，保持主体结构、哑光黑色金属外壳、四个风管接口和TRESOR标识的位置与字形。产品在暖灰摄影棚的专业吊顶设备展示支架上水平展示，产品底面朝向镜头，表现其扁平和精密，不安装到地板上使用，不改变为立式净化器。0–2秒极近距离沿一个圆形管口和机身边缘掠过，2–6秒镜头稳定退后，揭示完整机身与四个管口，6–7秒保持完整产品。柔和长条摄影灯在哑光表面形成克制移动的光影，精细倒角、真实接触阴影、温暖与科技兼具。不要拆解外壳，不得编造内部结构。无新增文字、数字、标注、界面、烟雾和激光。'
  item['prompt']=prompt;save()
  r=call(['node','create','video','--title',key+'｜'+title+'产品镜头｜仅一次','--mode','m2v','--model','seedance_2.0_fast_vip','--ratio','9:16','--resolution','720p','--duration','7','--count','1','--ref','node:'+item['referenceNodeId'],'--prompt',prompt])
  n=r['data']['node'];item.update(nodeId=n['nodeId'],phase='saved',upstreamNodeIds=n['upstreamNodeIds']);save();print(key,item['nodeId'],flush=True)
elif action=='quote':
 args=['node','quote']
 for key,*_ in products:args+=['--node-id',s['items'][key]['nodeId']]
 r=call(args);(base/'即梦记录/产品报价.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False))
elif action=='run':
 q=json.loads((base/'即梦记录/产品报价.json').read_text())['data'];total=q['totalMaxCredits'];assert total+s['committed']<=600
 assert all('maxCredits' in x and not x.get('error') for x in q['items'])
 ids=[];subs=[]
 for key,*_ in products:
  item=s['items'][key];assert item['generationCount']==0 and item['phase']=='saved';ids+=['--node-id',item['nodeId']];subs+=['--submit-id',item['submitId']]
 token=call(['node','confirm',*ids,'--credit-ceiling',str(total)])['data']['creditConfirmationToken']
 for key,*_ in products:
  item=s['items'][key];item.update(phase='submitting',generationCount=1,authorizedCreditCeiling=next(x['maxCredits'] for x in q['items'] if x['nodeId']==item['nodeId']))
 s['committed']+=total;save()
 r=call(['node','run',*ids,*subs,'--credit-token',token]);del token
 (base/'即梦记录/产品提交结果.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
 for x in r['data']['items']:
  item=next(v for v in s['items'].values() if v.get('nodeId')==x['nodeId']);item.update(phase=x['state'],operationRef=x['submitId'])
 save();print(json.dumps(r,ensure_ascii=False))
