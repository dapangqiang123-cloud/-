from pathlib import Path
import json,subprocess,sys,os
r=Path(__file__).resolve().parent;p=r/'G03_job_state.json';s=json.loads(p.read_text());cli='/Users/weipeilong/.local/bin/dreamina-canvas'
if s.get('video_generation_attempts',0):
 print('Already dispatched or uncertain; inspect original operation only:',s['videoSubmitId']);raise SystemExit(0)
q=json.loads((r/'G03_报价.json').read_text());ceiling=q['data']['totalMaxCredits']
assert q['ok'] and q['data']['confirmable'] and len(q['data']['items'])==1
assert q['data']['items'][0]['nodeId']==s['videoNodeId'] and ceiling==24
assert s['prior_budget_reservation']+ceiling<=s['total_budget']
a=subprocess.run([cli,'node','confirm','--project-id',s['projectId'],'--node-id',s['videoNodeId'],'--credit-ceiling',str(ceiling)],capture_output=True,text=True)
j=json.loads(a.stdout) if a.stdout else {'ok':False}
if not j.get('ok'):
 print('Credit confirmation failed; run was not called.');print(j.get('error',{}));raise SystemExit(a.returncode or 1)
token=j['data']['creditConfirmationToken']
s['authorized_credit_ceiling']=ceiling;s['conservative_reserved_total']=s['prior_budget_reservation']+ceiling;s['creditConfirmRequestId']=j.get('meta',{}).get('requestId');s['video_generation_attempts']=1;s['status']='run_dispatching_once_do_not_replay';p.write_text(json.dumps(s,ensure_ascii=False,indent=2));os.chmod(p,0o600)
a=subprocess.run([cli,'node','run','--project-id',s['projectId'],'--node-id',s['videoNodeId'],'--submit-id',s['videoSubmitId'],'--credit-token',token],capture_output=True,text=True)
del token,j

def redact(v):
 if isinstance(v,dict):return {k:redact(x) for k,x in v.items() if not any(t in k.lower() for t in ['token','url','provider','payload','body','draftcontent'])}
 if isinstance(v,list):return [redact(x) for x in v]
 return v
j=json.loads(a.stdout) if a.stdout else {'ok':False,'error':{'code':'no_json_response','requiredAction':'resume_original_operation'}}
safe=redact(j);(r/'G03_唯一提交回执.json').write_text(json.dumps(safe,ensure_ascii=False,indent=2));s['status']='submitted_observe_original_operation' if j.get('ok') else 'run_result_needs_read_only_recovery';s['runRequestId']=j.get('meta',{}).get('requestId');p.write_text(json.dumps(s,ensure_ascii=False,indent=2))
ledger=r.parent.parent/'assets/generated/生成台账.json';d=json.loads(ledger.read_text());d['video_calls']=1;d['remaining_calls_conservative']=4;d['jimeng_authorized_credit_ceiling_this_round']=ceiling;d['jimeng_budget_reservation_including_history']=s['conservative_reserved_total'];d['entries'].append({'id':'G03_video_once','type':'Seedance_2.0_Fast_720p','status':s['status'],'nodeId':s['videoNodeId'],'submitId':s['videoSubmitId'],'imageNodeId':s['imageNodeId'],'duration_seconds':4,'count':1,'authorized_ceiling':ceiling,'note':'这里只记录提交与上限，不把受理写成生成成功或最终净扣费。'});ledger.write_text(json.dumps(d,ensure_ascii=False,indent=2))
print(json.dumps(safe,ensure_ascii=False)[:3500]);raise SystemExit(a.returncode)
