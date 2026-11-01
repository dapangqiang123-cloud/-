from pathlib import Path
import json,subprocess,math,csv,sys,concurrent.futures
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np
ROOT=Path.cwd();BASE=ROOT/'家的空气答案/产出/20261027_第六期多空间选型_正式成片V2';WORK=BASE/'制作文件';V=BASE/'视频素材';P=BASE/'分段镜头/无文字';T=BASE/'分段镜头/有文字';CHECK=BASE/'检查';G=WORK/'图形叠层'
for p in [P,T,G]:p.mkdir(parents=True,exist_ok=True)
W,H,FPS=1080,1920,30
FORCE_TEXT='--force' in sys.argv
SERIF='/System/Library/Fonts/Supplemental/Songti.ttc';SANS='/System/Library/Fonts/Hiragino Sans GB.ttc'
def font(s,serif=False):return ImageFont.truetype(SERIF if serif else SANS,s,index=6 if serif else 0)
IV=(245,242,237);GOLD=(218,184,144);COFFEE=(59,47,44)
products=json.loads((WORK/'候选产品素材.json').read_text());official=lambda i:products[i]['path'];lib=lambda n:str(V/f'LibTV原始/视频节点 {n}.mp4')
A=str(V/'Seedance_A_客餐厅与C2.mp4');B=str(V/'Seedance_B_多空间净化新风.mp4')
rows=list(csv.DictReader(open(ROOT/'memory/projects/tresor-assets-files.csv',encoding='utf-8-sig')))
window=next(r['绝对路径'] for r in rows if r['文件名']=='5月15日 (1).mp4')
fixed=ROOT/'家的空气答案/产出/20261027_第六期多空间选型_全套分镜/风效修正版V2/分镜图'
ref12=next(fixed.glob('12_*'))
asset=Path('/Users/weipeilong/Downloads/本期视频参考素材分镜产品/产品图')
prods=[asset/'c2风管机右侧透视.png',asset/'c3多联机正视.jpg',asset/'c3d多联机2.png',asset/'mini新风2.png']
logo=ROOT/'品牌常用素材/璀璨/璀璨中央空调_logo.png'
shots=[]
def add(dur,name,source,inn=0,q=0,lines=(),sub='',layout='low',fx='',crop=None,zoom=1,gray=False,freeze=0,foot=''):
 at=sum(x['duration'] for x in shots);shots.append(dict(id=len(shots)+1,start=at,end=round(at+dur,3),duration=dur,name=name,source=str(source),inPoint=inn,q=q,lines=list(lines),sub=sub,layout=layout,fx=fx,crop=crop,zoom=zoom,gray=gray,freeze=freeze,foot=foot))
add(2,'装修选型_家庭实景',lib(6),.15,lines=['秋冬装修，'],sub='中央空调怎么选？')
add(2,'C2风扇细节_开篇',official(5),6.7,lines=['中央空调怎么选？'],sub='选之前，先看这四点',layout='low',crop=[1200,0,1215,2160])
add(5,'Q1_客餐厅大空间',lib(3),0,q=1,lines=['客餐厅一体，','大空间怎么选？'],sub='01 / 客餐厅一体 · 大空间')
add(8,'风量距离_覆盖过程',A,.35,q=1,lines=['看风量，也看距离'],sub='让舒适，从客厅延伸到餐厅',foot='气流效果示意')
add(5,'C2艺境_18米送风',A,9.6,q=1,lines=['璀璨 C2 艺境'],sub='18 m｜超远送风',layout='hero',foot='送风距离受内机型号、安装及实际工况影响')
add(5,'Q2_全屋选型',lib(2),0,q=2,lines=['全屋都想装，','中央空调怎么选？'],sub='02 / 多房间 · 多种需求')
add(5,'一拖多_分房运行',B,0,q=2,lines=['各个房间，按需开'],sub='一台外机，连接多个空间',foot='空间覆盖概念示意，非安装设计图')
add(3,'分房控制_品质舒适',B,1.7,q=2,lines=['产品品质'],sub='决定生活舒适度',zoom=1.5,foot='各屋独立控制示意')
add(2.5,'C3知境_室外机',lib(7),.1,q=2,lines=['璀璨 C3 知境'],sub='日系核心压缩机',layout='hero')
add(2.5,'C3_冷媒散热细节',official(7),70.15,q=2,lines=['冷媒散热'],sub='高温稳定运行',crop=[1090,0,607,1080],foot='技术效果示意')
add(5,'Q3_老人孩子',lib(8),0,q=3,lines=['家有老人孩子，','中央空调怎么选？'],sub='03 / 全家空气健康')
add(4,'空气污染_净化过程',B,5.12,q=3,lines=['空气净化能力是关键'],sub='关注甲醛、PM2.5、异味',fx='purify',foot='净化原理示意')
add(3.5,'Hi_nano_净化模块细节',official(4),10.9,q=3,lines=['Hi-nano Ultra'],sub='健康模块',gray=True,layout='hero',foot='技术效果示意')
add(1.5,'净化后_清透室内',B,7.5,q=3,lines=['除醛 · 除菌 · 除异味'],foot='净化效果受环境及使用条件影响')
add(4,'C3D_白色双风扇外机',official(1),0,q=3,lines=['璀璨 C3D 系列'],sub='Hi-nano Ultra 健康模块',layout='hero',zoom=1.25)
add(2,'三重净化_滤网微距',official(6),58.9,q=3,lines=['三重净化'],sub='除醛｜除菌｜除异味',crop=[420,0,607,1080],gray=True,foot='技术效果示意')
add(2,'Q4_秋日窗外',lib(5),0,q=4,lines=['秋冬常关窗，'],sub='04 / 新风 · 持续换气')
add(3,'Q4_关闭窗户',lib(5),2,q=4,lines=['怕憋闷，怎么选？'],sub='重点看新风换气能力')
add(3,'新风_双向风路',ref12,0,q=4,lines=['不开窗，也能换新空气'],sub='室外新风进入 · 室内浊气排出',fx='duct',foot='风路概念示意，非安装设计图')
add(5,'新风_暖白风幕入室',B,10.1,q=4,lines=['持续新风换气'],sub='把室外新鲜空气，送进来',freeze=.15,foot='气流效果示意')
add(3,'Mini_热交换过滤过程',official(0),57.7,q=4,lines=['璀璨 Mini 新风'],sub='三层过滤',gray=True,layout='hero',crop=[360,0,607,1080],foot='技术效果示意')
add(2,'Mini_产品与新风量','GRAPHIC_MINI',q=4,lines=['350 m³/h'],sub='大新风量 · 母婴级舒适新风',layout='mini',foot='性能与使用环境及实际工况有关')
add(3.5,'四款产品_选择答案','GRAPHIC_MATRIX',lines=['不同空间，不同家庭，','自然有不同答案。'],layout='matrix')
add(2.5,'品牌收束_家庭舒适',lib(8),2,q=0,lines=['让每一种舒适，','都选得恰到好处。'],layout='end',freeze=.5)
assert round(sum(s['duration'] for s in shots),3)==84
# 原始参考图复用，图像保持清晰；这里只做视频中的位置、气流与文字叠层。
def trim_asset(path,size):
 im=Image.open(path).convert('RGBA')
 if path.suffix.lower()=='.jpg':
  a=np.array(im);white=np.all(a[:,:,:3]>248,axis=2);mask=Image.fromarray((white*255).astype('uint8')).copy();ImageDraw.floodfill(mask,(0,0),128);outside=np.array(mask)==128;a[outside,3]=0;im=Image.fromarray(a,'RGBA')
 im=im.crop(im.getbbox());im.thumbnail(size,Image.Resampling.LANCZOS);return im
prodims=[trim_asset(x,(245,470)) for x in prods]
logim=trim_asset(logo,(540,200))
# opacity gradient for legible text, no opaque cards
shade=Image.new('RGBA',(W,H));a=np.zeros((H,W),dtype=np.uint8)
for y in range(H):
 a[y,:]=int(115*max(0,min(1,(y-950)/650)))
shade.putalpha(Image.fromarray(a));color=Image.new('RGBA',(W,H),COFFEE+(0,));color.putalpha(Image.fromarray(a));shade=color

def text(draw,xy,content,size=52,serif=False,fill=IV,anchor=None):
 ff=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',size) if '³' in content else font(size,serif)
 draw.text(xy,content,font=ff,fill=fill,stroke_width=0,anchor=anchor)

def overlay(s):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 if s['layout'] not in ['matrix','mini']:im.alpha_composite(shade)
 if s['layout']=='hero':
  # localized transparent top shading; product remains untouched
  grad=Image.new('RGBA',(W,H));ar=np.zeros((H,W),dtype=np.uint8)
  for y in range(200,760):ar[y,:]=int(60*math.sin(math.pi*(y-200)/560))
  grad.paste(COFFEE,(0,0,W,H));grad.putalpha(Image.fromarray(ar));im.alpha_composite(grad)
 d=ImageDraw.Draw(im)
 if s['layout']!='end':
  color=COFFEE if s['layout'] in ['matrix','mini'] else IV
  # subtle shadow on image backgrounds
  for tx,ty,msg,sz in [(72,232,'家的空气答案',31),(870,232,'第六期',28)]:
   if color==IV:d.text((tx+1,ty+2),msg,font=font(sz),fill=(38,30,27,150))
   text(d,(tx,ty),msg,sz,fill=color)
  d.line((72,292,1008,292),fill=color+(90,),width=1)
  if s['q']:
   for k in range(1,5):
    x=72+(k-1)*247;alpha=245 if k==s['q'] else 115
    d.line((x,1504,x+196,1504),fill=GOLD+(alpha,),width=3 if k==s['q'] else 1)
    text(d,(x,1516),'Q'+str(k),24,fill=(COFFEE if s['layout']=='mini' else IV)+(alpha,))
 layout=s['layout'];y=1195 if layout=='low' else 360
 if layout in ['mini','matrix']:y=350
 if layout=='end':
  tint=Image.new('RGBA',(W,H),COFFEE+(72,));im.alpha_composite(tint);im.alpha_composite(logim,((W-logim.width)//2,400));d=ImageDraw.Draw(im);y=1240
 if layout=='hero':
  for ln in s['lines']:text(d,(72,y),ln,62,serif=True);y+=85
  text(d,(72,y+14),s['sub'],64 if '18 m' in s['sub'] else 43)
 elif layout=='mini':
  text(d,(72,y),s['lines'][0],96,fill=COFFEE);text(d,(72,y+140),s['sub'],38,fill=COFFEE)
 elif layout=='matrix':
  for ln in s['lines']:text(d,(72,y),ln,57,serif=True,fill=COFFEE);y+=86
  for i,nm in enumerate(['C2 艺境','C3 知境','C3D 系列','Mini 新风']):text(d,(155+i*255,1470),nm,29,fill=COFFEE,anchor='mm')
 elif layout=='end':
  for ln in s['lines']:text(d,(W//2,y),ln,58,serif=True,anchor='mm');y+=90
  text(d,(W//2,1478),'家的空气答案 · 多空间选型',29,anchor='mm',fill=GOLD)
 else:
  if s['q'] and 'Q' in s['name']:
   text(d,(72,y-90),'Q'+str(s['q']),54,fill=GOLD)
  for ln in s['lines']:text(d,(72,y),ln,58 if len(ln)<15 else 51,serif=True);y+=82
  if s['sub']:text(d,(72,y+12),s['sub'],35 if len(s['sub'])>18 else 38,fill=IV)
 if s['foot']:text(d,(72,1448),s['foot'],22,fill=(COFFEE if s['layout']=='mini' else IV)+(190,))
 im.save(G/f'{s["id"]:02}.png')
for s in shots:overlay(s)

# Readable timing and sources. No tokens or temporary URLs.
(WORK/'镜头配置.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
(BASE/'timing.json').write_text(json.dumps({'duration':84,'width':W,'height':H,'fps':FPS,'audio':False,'scenes':shots,'generation':{'model':'seedance_2.0_fast_vip','resolution':'720p','count':2,'quotedMaxCredits':180,'authorizedMaxCredits':1500}},ensure_ascii=False,indent=2))

def encode_raw(s,framefn):
 out=P/f'{s["id"]:02}_{s["name"]}.mp4';p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','3','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 try:
  for n in range(round(s['duration']*FPS)):p.stdin.write(framefn(n/FPS).convert('RGB').tobytes())
  p.stdin.close();code=p.wait()
 except: p.kill();raise
 if code:raise RuntimeError(out)
 return out

def graphic(s):
 # restrained warm architectural light and four precise, original product assets
 yy,xx=np.mgrid[0:H,0:W];v=np.clip((xx+yy*.22)/1600,0,1)
 arr=np.stack([247-16*v,244-20*v,237-25*v],axis=2).astype('uint8');bg=Image.fromarray(arr,'RGB').convert('RGBA');dr=ImageDraw.Draw(bg)
 dr.polygon([(0,600),(1080,80),(1080,200),(0,740)],fill=(255,252,244,120));dr.line((0,1440,1080,1405),fill=(205,193,175,125),width=1)
 if s['source']=='GRAPHIC_MINI':
  mini=trim_asset(prods[3],(770,700))
  def fr(t):
   im=bg.copy();d=ImageDraw.Draw(im);y=840-int(16*math.sin(min(t/2,1)*math.pi/2));x=(W-mini.width)//2
   sh=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(sh);sd.ellipse((180,1260,900,1340),fill=(75,57,45,40));im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(28)));im.alpha_composite(mini,(x,y))
   for k in range(3):
    xx0=240+k*210;progress=max(0,min(1,(t-k*.23)/.6));d.line((xx0,1365,xx0+int(145*progress),1365),fill=(184,149,95,180),width=5)
   return im
 else:
  def fr(t):
   im=bg.copy();shadow=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(shadow)
   for i,a in enumerate(prodims):
    x=35+i*255+(245-a.width)//2;y=1420-a.height;op=max(0,min(1,(t-.12*i)/.55));dy=round((1-op)*60)
    sd.ellipse((x+8,1411,x+a.width+20,1441),fill=(80,60,45,int(45*op)))
   im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(15)))
   for i,a in enumerate(prodims):
    x=35+i*255+(245-a.width)//2;y=1420-a.height;op=max(0,min(1,(t-.12*i)/.55));dy=round((1-op)*60);a=a.copy();a.putalpha(a.getchannel('A').point(lambda v:int(v*op)));im.alpha_composite(a,(x,y+dy))
   return im
 return encode_raw(s,fr)

def duct(s):
 original=Image.open(s['source']).convert('RGB').resize((W,H),Image.Resampling.LANCZOS);ar=np.array(original);region=ar[310:470,180:830].astype(float)
 # Warm the cyan intake visualization only, preserving stone and device texture.
 m=(region[:,:,2]>region[:,:,0]*1.04)&(region[:,:,2]>100)
 lum=region.mean(2);warm=np.stack([lum*1.06,lum*1.025,lum*.96],2);region[m]=warm[m];ar[310:470,180:830]=np.clip(region,0,255).astype('uint8');original=Image.fromarray(ar).convert('RGBA')
 paths=[[(160,382),(520,388),(660,408),(710,485)],[(680,358),(650,290),(420,286),(160,275)]]
 def linepoint(pts,p):
  seg=[math.dist(a,b) for a,b in zip(pts,pts[1:])];tot=sum(seg);v=p*tot
  for a,b,d in zip(pts,pts[1:],seg):
   if v<=d:return (a[0]+(b[0]-a[0])*v/d,a[1]+(b[1]-a[1])*v/d)
   v-=d
  return pts[-1]
 def fr(t):
  im=original.copy();lay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(lay)
  for k,pts in enumerate(paths):
   for j in range(5):
    prog=(t*.40+j*.21)%1;x,y=linepoint(pts,prog);d.ellipse((x-5,y-3,x+5,y+3),fill=(255,244,220,195))
  # Tiny, flowing warm-white strands emerge from the correct face vent.
  for j in range(9):
   x0=525+j*52;pts=[]
   for z in range(30):
    p=z/29;y=550+p*300;x=x0+65*p*p+3*math.sin(t*1.6+p*5+j);pts.append((x,y))
   d.line(pts,fill=(255,244,224,22),width=2)
  im.alpha_composite(lay);return im
 return encode_raw(s,fr)

def render_plate(s):
 out=P/f'{s["id"]:02}_{s["name"]}.mp4'
 if out.exists() and out.stat().st_size>10000:return str(out)
 if s['source'].startswith('GRAPHIC'):return str(graphic(s))
 if s['fx']=='duct':return str(duct(s))
 args=['ffmpeg','-v','error','-y','-ss',str(s['inPoint']),'-i',s['source']]
 filters=[]
 if s['crop']:
  x,y,w,h=s['crop'];filters.append(f'crop={w}:{h}:{x}:{y}')
 z=s['zoom'];filters+=['fps=30',f'scale={round(W*z/2)*2}:{round(H*z/2)*2}:force_original_aspect_ratio=increase',f'crop={W}:{H}','setsar=1']
 if s['gray']:filters+=['hue=s=0','colorbalance=rs=.045:gs=.018:bs=-.035']
 if s['freeze']:
  activeframes=round((s['duration']-s['freeze'])*FPS);filters+=['trim=end_frame='+str(activeframes),'setpts=N/(30*TB)','loop=loop=-1:size=1:start='+str(activeframes-1),'setpts=N/(30*TB)']
 filters+=['format=yuv420p']
 args+=['-vf',','.join(filters),'-frames:v',str(round(s['duration']*FPS)),'-an','-c:v','libx264','-preset','fast','-crf','18','-threads','3','-r','30','-movflags','+faststart',str(out)]
 r=subprocess.run(args,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(s['name']+r.stderr[-1500:])
 return str(out)

def render_text(s):
 p=P/f'{s["id"]:02}_{s["name"]}.mp4';out=T/p.name
 if out.exists() and out.stat().st_size>10000 and not FORCE_TEXT:return str(out)
 # Text eases in over moving footage; picture cuts remain direct.
 cmd=['ffmpeg','-v','error','-y','-i',str(p),'-loop','1','-i',str(G/f'{s["id"]:02}.png'),'-filter_complex','[1:v]format=rgba,fade=t=in:st=0:d=0.22:alpha=1[txt];[0:v][txt]overlay=0:0:shortest=1,format=yuv420p[v]','-map','[v]','-frames:v',str(round(s['duration']*FPS)),'-an','-c:v','libx264','-preset','fast','-crf','18','-threads','3','-r','30','-movflags','+faststart',str(out)]
 r=subprocess.run(cmd,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr[-1500:])
 return str(out)

def concat(folder,out):
 fs=[folder/f'{s["id"]:02}_{s["name"]}.mp4' for s in shots];lst=WORK/(out.stem+'_concat.txt');lst.write_text('\n'.join("file '"+str(f).replace("'","'\\''")+"'" for f in fs))
 subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-an','-movflags','+faststart',str(out)],check=True)
if __name__=='__main__':
 mode=sys.argv[1] if len(sys.argv)>1 else 'all'
 if mode in ['all','plate']:
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
   for out in ex.map(render_plate,shots):print('PLATE',Path(out).name,flush=True)
  concat(P,BASE/'textless_plate.mp4')
 if mode in ['all','text']:
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
   for out in ex.map(render_text,shots):print('TEXT',Path(out).name,flush=True)
  concat(T,BASE/'final_with_text.mp4')
 print('DONE',flush=True)
