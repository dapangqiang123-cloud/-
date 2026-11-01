import json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
b=Path(__file__).parent;o=b/'精细选片';o.mkdir(exist_ok=True)
idx={i['id']:i for i in json.loads((b/'达人选片/index.json').read_text())}
sets={11:[0,3,12,14,16,18,84,88,90,115,117,119],17:[8,10,12,14,16,18,20,22,50,54,58,68],15:[50,52,54,56,58,60,68,70,72,74,76,78],20:[60,62,64,66,68,70,72,74,76,78,80,82],5:[48,50,52,54,56,58,60,64,68,70,74,76]}
for id,ts in sets.items():
 sh=Image.new('RGB',(1200,4*380),(20,20,20));d=ImageDraw.Draw(sh)
 for j,t in enumerate(ts):
  p=o/f'{id}_{t}.jpg';subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',idx[id]['path'],'-frames:v','1','-vf','scale=390:350:force_original_aspect_ratio=decrease','-y',str(p)],check=True)
  im=Image.open(p);x=j%3*400+(400-im.width)//2;y=j//3*380;sh.paste(im,(x,y));d.text((j%3*400+10,y+355),f'{id} | {t}s',fill='white')
 sh.save(o/f'{id}_contact.jpg');print(id,flush=True)
