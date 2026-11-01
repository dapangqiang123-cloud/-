from pathlib import Path
import json,subprocess,sys
r=Path(__file__).resolve().parent;p=r/'G03_job_state.json';s=json.loads(p.read_text())
if s.get('videoNodeId'):
 print('Video node already exists; no create:',s['videoNodeId']);raise SystemExit(0)
prompt=(r/'G03_视频提示词_4秒.txt').read_text();prompt=prompt.replace('以已上传的G03明亮米白浅木三房住宅图片为唯一首帧与建筑锚点', '以{{node:'+s['imageNodeId']+'}}这张已确认的明亮米白浅木三房住宅图片为唯一首帧与建筑锚点')
(r/'G03_实际视频提示词_含图片节点.txt').write_text(prompt)
cmd=['/Users/weipeilong/.local/bin/dreamina-canvas','node','create','video','--project-id',s['projectId'],'--update-id',s['videoUpdateId'],'--title','G03 明亮三房｜4秒动态样片·只生成一次','--mode','first_last_frame','--model',s['model'],'--ratio','9:16','--resolution','720p','--duration','4','--count','1','--prompt',prompt,'--ref','node:'+s['imageNodeId']]
a=subprocess.run(cmd,capture_output=True,text=True)
def redact(v):
 if isinstance(v,dict):return {k:redact(x) for k,x in v.items() if not any(t in k.lower() for t in ['token','url','provider','payload','body','draftcontent'])}
 if isinstance(v,list):return [redact(x) for x in v]
 return v
j=json.loads(a.stdout) if a.stdout else {'ok':False,'stderr':a.stderr[:2000]};(r/'G03_视频节点保存.json').write_text(json.dumps(redact(j),ensure_ascii=False,indent=2))
if j.get('ok'):
 n=j['data']['node'];s['videoNodeId']=n['nodeId'];s['status']='video_node_saved_not_generated';s['saveRequestId']=j.get('meta',{}).get('requestId');p.write_text(json.dumps(s,ensure_ascii=False,indent=2));print(json.dumps({'ok':True,'nodeId':n['nodeId'],'type':n.get('type'),'upstreamNodeIds':n.get('upstreamNodeIds'),'generation':redact(n.get('generation',{}))},ensure_ascii=False))
else:print(json.dumps(redact(j),ensure_ascii=False))
raise SystemExit(a.returncode)
