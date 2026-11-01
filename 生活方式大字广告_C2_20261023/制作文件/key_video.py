"""Local compositing only. No AI calls and no regeneration."""
from pathlib import Path
import subprocess,json
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'可编辑工程/assets'
excess='g(X,Y)-max(r(X,Y),b(X,Y))'
# The dining generation added a light on its green screen. An RGB difference
# matte removes both bright and dark greens; a bounded relaxed threshold keeps
# the thin olive-toned vase branches. Wardrobe/skin stay outside green hues.
dining_alpha=f"if(lt(Y,65)+lt(X,265)*lt(Y,290),0,if(between(X,480,650)*between(Y,240,360),255*(1-clip(({excess}-50)/30,0,1)),255*(1-clip(({excess}-3)/16,0,1))))"
filters={
 'lounge':'fps=30,chromakey=0x00FF00:0.17:0.045,despill=type=green:mix=0.65:expand=0.01',
 'dining':f"fps=30,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='{dining_alpha}',despill=type=green:mix=0.6:expand=0.01",
}
specs=[('lounge','05_客厅_Seedance2Fast_唯一一次.mp4'),('dining','06_餐厅_Seedance2Fast_唯一一次.mp4')]
facts=[]
for key,name in specs:
 src=ROOT/'素材'/name;out=A/f'{key}_alpha.mov'
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(src)]))
 facts.append({'key':key,'source':str(src),'streams':[{k:s.get(k) for k in ['codec_type','codec_name','width','height','r_frame_rate','duration']} for s in meta['streams']]})
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-t','6','-an','-vf',filters[key],'-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le','-alpha_bits','16','-threads','2',str(out)],check=True)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss','5.95','-i',str(out),'-frames:v','1','-y',str(A/f'{key}_end.png')],check=True)
 print(key,'keyed to ProRes4444 alpha')
(ROOT/'制作文件/媒体参数.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2))
