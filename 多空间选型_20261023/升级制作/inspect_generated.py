import subprocess,json
from PIL import Image,ImageDraw
from pathlib import Path
b=Path(__file__).parent;o=b/'生成检查';o.mkdir(exist_ok=True)
for p in sorted((b/'即梦生成素材').glob('*.mp4')):
 sheet=Image.new('RGB',(1080,840),(25,25,25));d=ImageDraw.Draw(sheet)
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]));dur=float(meta['format']['duration'])
 for j,f in enumerate([.04,.2,.4,.6,.8,.96]):
  t=dur*f;dest=o/f'{p.stem}_{t:.2f}.jpg';subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=350:390:force_original_aspect_ratio=decrease','-y',str(dest)],check=True)
  im=Image.open(dest);sheet.paste(im,((j%3)*360+(360-im.width)//2,(j//3)*420));d.text(((j%3)*360+10,(j//3)*420+395),f'{p.stem} {t:.2f}s',fill='white')
 sheet.save(o/f'{p.stem}_contact.jpg',quality=90);print(p.stem,dur,flush=True)
