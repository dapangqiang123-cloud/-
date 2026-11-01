"""Inspect a downloaded source, create silent review output, and extract targeted QA frames."""
from pathlib import Path
import argparse,json,subprocess
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--sample',type=Path,required=True);a=p.parse_args();r=Path(__file__).resolve().parent;qa=r.parent/'G03_动态审阅';qa.mkdir(exist_ok=True);a.sample.parent.mkdir(exist_ok=True)
def probe(path):
 z=subprocess.run(['/opt/homebrew/bin/ffprobe','-v','error','-count_frames','-show_entries','format=duration:stream=index,codec_type,codec_name,width,height,avg_frame_rate,nb_read_frames','-of','json',str(path)],check=True,capture_output=True,text=True);return json.loads(z.stdout)
s=probe(a.source);(qa/'原始视频_ffprobe.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
# Normal delivery scaling only, no sharpening or frame interpolation that could distort geometry.
subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-i',str(a.source),'-map','0:v:0','-an','-sn','-dn','-vf','scale=1080:1920:flags=lanczos,fps=30,format=yuv420p','-t','4','-c:v','libx264','-crf','18','-preset','slow','-movflags','+faststart',str(a.sample)],check=True)
t=probe(a.sample);v=next(x for x in t['streams'] if x['codec_type']=='video');assert v['width']==1080 and v['height']==1920 and v['avg_frame_rate']=='30/1';assert not any(x['codec_type']=='audio' for x in t['streams']);assert abs(float(t['format']['duration'])-4)<1/30;assert int(v['nb_read_frames'])==120
(qa/'样片_ffprobe.json').write_text(json.dumps(t,ensure_ascii=False,indent=2));times=[0,.5,1,1.5,2,2.5,3,3.5,3.966];sheet=Image.new('RGB',(1080,2010),(245,242,237));draw=ImageDraw.Draw(sheet);black=[]
for i,time in enumerate(times):
 f=qa/f'frame_{i:02d}_{time:.3f}.png';subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-ss',str(time),'-i',str(a.sample),'-frames:v','1',str(f)],check=True);im=Image.open(f).convert('RGB');black.append({'time':time,'pure_black_pixels':sum(q==(0,0,0) for q in im.getdata())});im.thumbnail((350,623));x=(i%3)*360+5;y=(i//3)*670;sheet.paste(im,(x,y));draw.text((x,y+632),f'{time:.3f}s',fill=(59,47,44))
sheet.save(qa/'G03_九帧审阅.jpg',quality=94);(qa/'抽帧黑色像素检查.json').write_text(json.dumps(black,ensure_ascii=False,indent=2));print(json.dumps({'source_probe':s,'sample_probe':t,'black_checks':black,'contact_sheet':str(qa/'G03_九帧审阅.jpg')},ensure_ascii=False))
