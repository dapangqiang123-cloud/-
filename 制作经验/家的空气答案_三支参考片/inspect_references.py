from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
files=[('01_energy','/Users/weipeilong/Desktop/璀璨中央空调/璀璨日常整理留存/8月/视频/产品卖点/家的空气答案 省电篇.mp4'),('02_system','/Users/weipeilong/Desktop/璀璨中央空调/璀璨日常整理留存/9月/视频/产品卖点、科普系列/家的空气答案 选多联机单元机.mp4'),('03_50sqm','/Users/weipeilong/Desktop/璀璨中央空调/璀璨日常整理留存/9月/视频/产品卖点、科普系列/家的空气答案50m²篇.mp4')]
metadata=[]
for name,path in files:
 d=root/name;d.mkdir(exist_ok=True)
 info=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_format','-show_streams','-of','json',path]));duration=float(info['format']['duration']);metadata.append({'id':name,'path':path,'probe':info})
 times=[round(.8+i*3.5,2) for i in range(int((duration-.8)/3.5)+1)]+[round(duration-.5,2)]
 for i,t in enumerate(times):subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-ss',str(t),'-i',path,'-frames:v','1','-vf','scale=540:-1','-q:v','2','-y',str(d/f'{i:02d}_{t}.jpg')],check=True)
 for pg in range((len(times)+11)//12):
  sub=times[pg*12:(pg+1)*12];canvas=Image.new('RGB',(4*270,3*505),'#202020');draw=ImageDraw.Draw(canvas)
  for j,t in enumerate(sub):
   i=pg*12+j;im=Image.open(d/f'{i:02d}_{t}.jpg');im.thumbnail((270,480));x=j%4*270;y=j//4*505;canvas.paste(im,(x,y+22));draw.text((x+8,y+5),f'{name} / {t}s',fill='white')
  canvas.save(d/f'contact_{pg+1}.jpg',quality=92)
 print(name,duration,len(times),flush=True)
(root/'原片索引.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
