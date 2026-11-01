import sys,json,shutil
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
sys.path.append('/Users/weipeilong/.cache/uv/archive-v0/JhWre3gpr50fylF3PAsaU')
import cv2
R=Path(__file__).resolve().parents[1];A=R/'OpenFilm工程/assets';A.mkdir(parents=True,exist_ok=True)
for k in ['room','hand']:
 im=Image.open(R/'素材'/f'{k}.png').convert('RGB');ar=np.array(im);h,w=ar.shape[:2]
 neutral=(ar.max(2).astype(int)-ar.min(2).astype(int)<17)
 candidate=((ar.min(2)>240)&neutral).astype('uint8')*255
 flood=candidate.copy();cv2.floodFill(flood,None,(0,0),128);bg=flood==128
 mask=np.where(bg,0,255).astype('uint8');mask=cv2.GaussianBlur(mask,(3,3),.5)
 
 if k=='room':
  mask[:]=0;mask[int(.168*h):int(.836*h),int(.122*w):int(.878*w)]=255
 out=Image.fromarray(np.dstack([ar,mask]));out=out.crop(out.getbbox());out.save(A/f'{k}.png');print(k,out.size)
for src,name in [(R.parent/'家的空气答案/产品素材/mini新风系统/1.png','mini.png'),(R.parent/'品牌常用素材/璀璨/璀璨中央空调_logo.png','logo.png')]:
 im=Image.open(src).convert('RGBA');im=im.crop(im.getbbox());im.save(A/name)
# Paper texture is original deterministic procedural material, not copied stock.
rng=np.random.default_rng(38);noise=rng.normal(0,1.5,(1920,1080,1));base=np.array([240,236,225])[None,None,:];ar=np.uint8(np.clip(base+noise,0,255));Image.fromarray(ar).save(A/'paper.jpg',quality=96)
# Existing locally supplied fonts; retain original family names in the source.
font=R.parent/'生活方式大字广告_C2_20261023/可编辑工程/assets/body.woff2'
if font.exists():shutil.copy2(font,A/'body.woff2')
print('Prepared',A)
