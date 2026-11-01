from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parent.parent
video=root/'璀璨多空间选型_9比16_84秒_女声样片_V1.mp4'
out=root/'成片检查'; out.mkdir(exist_ok=True)
probe=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
(out/'视频参数.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2))
v=next(s for s in probe['streams'] if s['codec_type']=='video')
a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'])==(1080,1920)
assert abs(float(probe['format']['duration'])-84)<.15
assert v['r_frame_rate']=='30/1'
times=[0,2.5,7.5,13,19,25,29.5,36.5,43.5,48.5,55.5,62.5,68,75,81,83.8]
for i,t in enumerate(times):
 subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1','-q:v','2','-y',str(out/f'{i:02d}_{t}s.jpg')],check=True)
for page,items in enumerate([list(enumerate(times))[:8],list(enumerate(times))[8:]]):
 canvas=Image.new('RGB',(4*270,2*510),'#222222');draw=ImageDraw.Draw(canvas)
 for pos,(i,t) in enumerate(items):
  im=Image.open(out/f'{i:02d}_{t}s.jpg');im.thumbnail((270,480))
  x=(pos%4)*270;y=(pos//4)*510;canvas.paste(im,(x,y+25));draw.text((x+8,y+6),f'{t}s',fill='white')
 canvas.save(out/f'成片画面检查_{page+1}.jpg',quality=94)
print(json.dumps({'duration':probe['format']['duration'],'dimensions':[v['width'],v['height']],'fps':v['r_frame_rate'],'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'size_MB':round(video.stat().st_size/1e6,2),'frames_checked':len(times)},ensure_ascii=False))
