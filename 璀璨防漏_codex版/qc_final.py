from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json,hashlib
R=Path(__file__).resolve().parent;Q=R/'output/质检';Q.mkdir(exist_ok=True)
f=R/'output/CC_20261028_家的空气答案06_双重防漏_v1.mp4'
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(f)]))
(R/'logs/最终ffprobe.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
v=next(x for x in meta['streams'] if x['codec_type']=='video');a=next(x for x in meta['streams'] if x['codec_type']=='audio')
assert(v['width'],v['height'])==(1080,1920)
assert v['avg_frame_rate']=='30/1'
assert abs(float(meta['format']['duration'])-65)<.05
assert int(v['nb_frames'])==1950
checks={'duration':meta['format']['duration'],'width':1080,'height':1920,'frame_rate':v['avg_frame_rate'],'frames':v['nb_frames'],'audio_sample_rate':a['sample_rate'],'audio_channels':a['channels'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
(R/'logs/最终参数核验.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
# Full decode checks every frame, independently of visual sampling.
p=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vf','blackdetect=d=0.08:pix_th=0.06:pic_th=0.98','-af','volumedetect','-f','null','-'],capture_output=True,text=True)
(R/'logs/完整解码与黑帧检查.log').write_text(p.stderr)
assert p.returncode==0
for suffix,times in [('每5秒',[*range(0,65,5),64.9]),('关键结构',[32,37.9,38,41,43.9,44,47,50.9,51.6,53.4,54.8,55.1,57.9])]:
 cols=4;rows=(len(times)+cols-1)//cols;c=Image.new('RGB',(cols*270,rows*504),'#ece8e2');d=ImageDraw.Draw(c)
 for i,t in enumerate(times):
  out=Q/f'final_{t:04.1f}s.jpg'
  subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(f),'-frames:v','1','-q:v','2',str(out)],check=True)
  im=Image.open(out);im.thumbnail((270,480));x=i%cols*270;y=i//cols*504;c.paste(im,(x,y));d.text((x+8,y+483),f'{t:04.1f} s',fill='black')
 c.save(Q/f'最终_{suffix}抽帧.jpg',quality=95)
print(json.dumps(checks,ensure_ascii=False))
