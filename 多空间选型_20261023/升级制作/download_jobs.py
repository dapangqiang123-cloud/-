from pathlib import Path
import json,subprocess
base=Path(__file__).parent;sp=base/'即梦记录/状态.json';s=json.loads(sp.read_text());out=base/'即梦生成素材';out.mkdir(exist_ok=True)
for key,item in s['items'].items():
 f=base/'即梦记录'/f'{key}_状态.json'
 if not f.exists():continue
 r=json.loads(f.read_text())['data']
 if r.get('state')!='succeeded':continue
 rid=r['resources'][0]['resourceId'];dest=out/(key+('.mp3' if item['type']=='audio' else '.mp4'))
 if dest.exists() and dest.stat().st_size>1000:continue
 p=subprocess.run(['dreamina-canvas','resource','download',rid,'--project-id',s['projectId'],'--output',str(dest)],capture_output=True,text=True)
 res=json.loads(p.stdout.strip() or p.stderr.strip())
 if not res.get('ok'):print(res);raise SystemExit(1)
 (base/'即梦记录'/f'{key}_下载.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));item.update(resourceId=rid,downloadedPath=str(dest),phase='succeeded');sp.write_text(json.dumps(s,ensure_ascii=False,indent=2));print(key,dest.stat().st_size,flush=True)
