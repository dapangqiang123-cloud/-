from pathlib import Path
import json, subprocess, random
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parent
M=json.loads((ROOT/'素材清单.json').read_text())
assets={m['id']:Image.open(ROOT/'素材'/m['name']).convert('RGBA') for m in M}
bg=assets[8]
ref1=Image.open(ROOT/'参考图'/'图1.jpg').convert('RGB')
ref2=Image.open(ROOT/'参考图'/'图2.jpg').convert('RGB')
numids=[17,14,11,15,12,9,16,13,10]
itemids=[3,1,4,0,2,18,5,7,6]
numguess=[(88+357*c,546+290*r) for r in range(3) for c in range(3)]
itemguess=[(158,547),(445,546),(846,583),(60,832),(465,864),(800,865),(94,1134),(516,1132),(794,1103)]

def fit(im,ref,guess):
 arr=np.array(im).astype(np.float32)
 yy,xx=np.where(arr[:,:,3]>220)
 rng=np.random.default_rng(42); ix=rng.choice(len(xx),min(700,len(xx)),replace=False); yy,xx=yy[ix],xx[ix]
 a=arr[yy,xx,3:4]/255; color=arr[yy,xx,:3]*a
 b=np.array(bg).astype(np.float32)[:,:,:3]; r=np.array(ref).astype(np.float32)
 best=(float('inf'),None)
 for y in range(guess[1]-15,guess[1]+16):
  for x in range(guess[0]-15,guess[0]+16):
   pred=color+(1-a)*b[yy+y,xx+x]
   err=np.mean((pred-r[yy+y,xx+x])**2)
   if err<best[0]: best=(float(err),(x,y))
 return best
numpos=[];itempos=[]
for i in range(9):
 e,p=fit(assets[numids[i]],ref1,numguess[i]);numpos.append(p);print('number',i+1,p,round(e,2),flush=True)
 e,p=fit(assets[itemids[i]],ref2,itemguess[i]);itempos.append(p);print('item',i+1,p,round(e,2),flush=True)

def compose(reveal=None,all_items=False):
 im=bg.copy()
 for i in range(9):
  show=all_items or reveal==i+1
  im.alpha_composite(assets[(itemids if show else numids)[i]],(itempos if show else numpos)[i])
 return im.convert('RGB')
frames=ROOT/'画面';frames.mkdir(exist_ok=True)
compose().save(frames/'数字牌.png')
compose(all_items=True).save(frames/'物品位置校对.png')
for n in range(1,10):compose(n).save(frames/f'闪现_{n}.png')
order=[5,2,8,4,1,9,3,7,6]
fps=30; sequence=[(None,6)]
for n in order:sequence.extend([(n,9),(None,2)])
sequence.append((None,15))
assert sum(n for _,n in sequence)==120
metadata={'resolution':[1200,1600],'fps':fps,'duration':4,'order':order,'number_asset_ids':numids,'item_asset_ids':itemids,'number_positions':numpos,'item_positions':itempos,'sequence':sequence}
(ROOT/'时间线.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
cmd=['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','warning','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','1200x1600','-framerate',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','slow','-crf','15','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'周五更璀璨_万圣节记忆挑战_4秒.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for n,count in sequence:
 data=compose(n).tobytes()
 for _ in range(count):p.stdin.write(data)
p.stdin.close()
assert p.wait()==0
print('RENDERED',flush=True)
