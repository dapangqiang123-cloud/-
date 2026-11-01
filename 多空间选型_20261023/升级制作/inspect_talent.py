import subprocess,json,concurrent.futures
from pathlib import Path
from PIL import Image,ImageDraw
root=Path('/Users/weipeilong/Desktop/璀璨中央空调/资料&客户提供/视频:达人素材/打包/打包素材/视频2')
out=Path(__file__).parent/'达人选片';out.mkdir(exist_ok=True)
files=sorted([p for p in root.iterdir() if p.suffix.lower() in ['.mp4','.mov','.m4v']])
def process(pair):
 i,p=pair
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]))
 d=float(meta['format']['duration']);v=next(s for s in meta['streams'] if s['codec_type']=='video')
 folder=out/f'{i:02d}';folder.mkdir(exist_ok=True)
 times=[d*x for x in [.04,.14,.25,.37,.49,.61,.73,.85,.95]]
 sheet=Image.new('RGB',(1080,3*400),(25,25,25));draw=ImageDraw.Draw(sheet)
 for j,t in enumerate(times):
  f=folder/f'{t:.2f}.jpg'
  if not f.exists():subprocess.run(['ffmpeg','-loglevel','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=350:370:force_original_aspect_ratio=decrease','-q:v','3','-y',str(f)],check=True)
  im=Image.open(f);x=(j%3)*360+(360-im.width)//2;y=(j//3)*400
  sheet.paste(im,(x,y));draw.text(((j%3)*360+10,y+375),f'{i:02d} | {t:.2f}s',fill='white')
 sheet.save(out/f'{i:02d}_contact.jpg',quality=86)
 print(i,p.name,round(d,2),flush=True)
 return {'id':i,'path':str(p),'duration':d,'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'times':times}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(process,enumerate(files,1)))
(out/'index.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
