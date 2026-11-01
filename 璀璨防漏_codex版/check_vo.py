from faster_whisper import WhisperModel
from pathlib import Path
import json,shutil,subprocess,numpy as np
R=Path(__file__).resolve().parent;p=Path('/Users/weipeilong/Downloads/JianyingPro Drafts/家的空气答案系列/textReading')
fs=sorted(p.glob('*'),key=lambda x:x.stat().st_mtime)[-10:]
model=WhisperModel('tiny',device='cpu',compute_type='int8',cpu_threads=3,download_root=str(R/'logs/whisper_model'))
out=[]
for f in fs:
 samples=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-f','f32le','-ac','1','-ar','16000','pipe:1']),dtype=np.float32)
 seg,info=model.transcribe(samples,language='zh',beam_size=5,vad_filter=False)
 txt=''.join(s.text for s in seg);print(f.name,txt,flush=True);out.append({'file':str(f),'text':txt})
 (R/'logs/VO核对转写.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
