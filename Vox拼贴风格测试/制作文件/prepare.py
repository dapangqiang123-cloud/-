import sys,json,shutil
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
sys.path.append('/Users/weipeilong/.cache/uv/archive-v0/JhWre3gpr50fylF3PAsaU')
import cv2
R=Path(__file__).resolve().parents[1];A=R/'OpenFilm工程/assets';A.mkdir(parents=True,exist_ok=True)
for k in ['mountain','forest','leaf','chair']:
 im=Image.open(R/'素材'/f'{k}.png').convert('RGB');ar=np.array(im);h,w=ar.shape[:2]
 # Flood only neutral, near-white pixels connected to the canvas border.
 neutral=(ar.max(2).astype(int)-ar.min(2).astype(int)<20)
 candidate=((ar.min(2)>235)&neutral).astype('uint8')*255
 flood=candidate.copy();cv2.floodFill(flood,None,(0,0),128);bg=flood==128
 mask=np.where(bg,0,255).astype('uint8')
 if k=='chair':
  # A photographed chair/lamp silhouette excludes its soft studio floor shadow.
  points=[(80,346),(98,326),(149,309),(164,287),(177,265),(181,220),(193,190),(215,175),(244,174),(265,185),(276,207),(274,252),(269,275),(280,287),(304,287),(319,278),(341,291),(368,316),(402,330),(432,352),(468,384),(508,421),(548,438),(565,430),(566,442),(557,453),(574,455),(601,473),(618,499),(615,553),(605,584),(583,604),(553,618),(501,622),(468,616),(435,598),(421,580),(411,556),(397,550),(379,552),(345,567),(308,575),(267,577),(222,574),(184,565),(157,550),(134,549),(109,537),(95,515),(86,486),(80,443)]
  p=Image.new('L',im.size);d=ImageDraw.Draw(p);d.polygon([(int(x*w/700),int(y*h/700)) for x,y in points],fill=255)
  # Lamp stalk and head are their own narrow photographic piece.
  d.polygon([(int(x*w/700),int(y*h/700)) for x,y in [(413,177),(474,175),(504,178),(511,187),(512,420),(505,421),(503,187),(470,184),(467,190),(413,190)]],fill=255)
  mask=np.minimum(mask,np.array(p))
 # Keep antialiasing without blurring photographic detail.
 mask=cv2.GaussianBlur(mask,(3,3),.55)
 rgba=np.dstack([ar,mask]);out=Image.fromarray(rgba);bb=out.getbbox();out=out.crop(bb);out.save(A/f'{k}.png');print(k,out.size)
shutil.copy2(R/'素材/room.png',A/'room.png')
for src,name in [(R.parent/'家的空气答案/产品素材/mini新风系统/1.png','mini.png'),(R.parent/'品牌常用素材/璀璨/璀璨中央空调_logo.png','logo.png')]:
 im=Image.open(src).convert('RGBA');im=im.crop(im.getbbox());im.save(A/name)
# Paper texture is original deterministic procedural material, not copied stock.
rng=np.random.default_rng(38);noise=rng.normal(0,1.5,(1080,1920,1));base=np.array([240,236,225])[None,None,:];ar=np.uint8(np.clip(base+noise,0,255));Image.fromarray(ar).save(A/'paper.jpg',quality=96)
# Existing locally supplied fonts; retain original family names in the source.
font=R.parent/'生活方式大字广告_C2_20261023/可编辑工程/assets/body.woff2'
if font.exists():shutil.copy2(font,A/'body.woff2')
print('Prepared',A)
