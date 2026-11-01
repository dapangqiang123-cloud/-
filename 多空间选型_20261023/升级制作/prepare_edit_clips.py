import json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
b=Path(__file__).parent;o=b/'剪映交付素材/视频片段';o.mkdir(exist_ok=True);shots=json.loads((b/'剪辑镜头表.json').read_text());src=b/'视觉母版_无字幕无声.mp4'
def go(s):
 dest=o/f'V{s["id"]:02}.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(s['at']),'-i',str(src),'-t',str(s['duration']),'-an','-c:v','h264_videotoolbox','-b:v','16M','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True)
 print(dest.name,s['name'],flush=True)
with ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(go,shots))
