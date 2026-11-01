from pathlib import Path
import subprocess
from PIL import Image,ImageDraw
b=Path.cwd()/'多空间选型_20261023/升级制作';d=b/'剪映交付素材/正式镜头';o=b/'正式镜头检查';o.mkdir(exist_ok=True)
for pg in range(3):
 im=Image.new('RGB',(1080,9*240),(24,24,24));draw=ImageDraw.Draw(im)
 for i in range(pg*9+1,pg*9+10):
  f=d/f'F{i:02}.mp4';dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(f)]))
  for j,t in enumerate([.08,dur/2,dur-.08]):
   dest=o/f'{i:02}_{j}.jpg';subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(f),'-frames:v','1','-vf','scale=120:214','-y',str(dest)],check=True)
   im.paste(Image.open(dest),(j*360+110,((i-1)%9)*240));draw.text((j*360+10,((i-1)%9)*240+215),f'V{i:02} {t:.2f}',fill='white')
 im.save(o/f'page{pg+1}.jpg',quality=90)
print(o)
