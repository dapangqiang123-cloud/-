from pathlib import Path
import json,subprocess,sys
r=Path(__file__).resolve().parent;p=r/'G03_job_state.json';s=json.loads(p.read_text())
cmd=['/Users/weipeilong/.local/bin/dreamina-canvas','node','create','text','--project-id',s['projectId'],'--update-id',s['textUpdateId'],'--title','G03 明亮三房｜首帧已确认·4秒视频提示词与预算','--text',(r/'画布说明正文.md').read_text(),'--import-kind','external_generated','--x','-720','--y','0']
a=subprocess.run(cmd,capture_output=True,text=True)
if a.stdout:
 try:
  j=json.loads(a.stdout);(r/'画布说明保存.json').write_text(json.dumps(j,ensure_ascii=False,indent=2));print(json.dumps(j,ensure_ascii=False)[:1000])
 except json.JSONDecodeError:print('Non-JSON response; not persisted')
if a.stderr:print(a.stderr[:1500],file=sys.stderr)
raise SystemExit(a.returncode)
