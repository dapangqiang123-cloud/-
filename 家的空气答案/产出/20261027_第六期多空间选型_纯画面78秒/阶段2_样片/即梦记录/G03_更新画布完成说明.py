from pathlib import Path
import json,uuid,subprocess
r=Path(__file__).resolve().parent;b=r.parent.parent;p=r/'G03_job_state.json';s=json.loads(p.read_text());s.setdefault('completedNoteUpdateId',str(uuid.uuid4()));p.write_text(json.dumps(s,ensure_ascii=False,indent=2))
text='''# G03 明亮三房｜第一段动态样片已完成，待用户确认

首帧由用户确认并手动上传，已核对与本地原图逐像素一致；此前CLI上传故障已恢复。

模型Seedance 2.0 Fast /720p /4秒 /9:16 /数量1。此镜只生成一次，没有上传参考视频。视频节点与图片节点的上游引用、正文引用和连线已回读核对。

资源记录24积分，历史保守预留516，累计540/600，保守余60；不是已经核实的账户最终净结算。保守生成计数3次图片+1次视频，8次上限余4次。

平台原视频720×1280且附带AAC音轨；交审文件已完整去音轨并转为1080×1920、30fps、4秒120帧。做轻微咖色阴影曲线避免纯黑像素，不改建筑。代表静帧及视频保存在璀璨总项目阶段2样片目录。其余五段代表样片与全片尚未完成。

## 实际视频提示词（绑定当前首帧）

'''+(r/'G03_实际视频提示词_含图片节点.txt').read_text()+'\n\n## ChatGPT首帧原提示词\n\n'+(b/'assets/generated/G03_三房剖切_首帧提示词_v3_明亮版.txt').read_text()
(r/'画布说明正文_已完成.md').write_text(text)
a=subprocess.run(['/Users/weipeilong/.local/bin/dreamina-canvas','node','edit','text','--project-id',s['projectId'],'--node-id',s['canvasNoteNodeId'],'--update-id',s['completedNoteUpdateId'],'--title','G03 明亮三房｜4秒样片已完成·24积分·待确认','--text',text],capture_output=True,text=True);j=json.loads(a.stdout) if a.stdout else {'ok':False};(r/'画布说明完成更新.json').write_text(json.dumps(j,ensure_ascii=False,indent=2));print(json.dumps({'ok':j.get('ok'),'requestId':j.get('meta',{}).get('requestId')},ensure_ascii=False));raise SystemExit(a.returncode)
