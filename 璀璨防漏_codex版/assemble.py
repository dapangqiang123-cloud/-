from pathlib import Path
import subprocess,json,sys
R=Path(__file__).resolve().parent;A=R/'assets';E=R/'edit/分镜视频';E.mkdir(exist_ok=True)
OLD=R.parent/'家的空气答案/产出/20261028_第六期双重防漏_开头快切/剪映分镜'
OFF=R.parent/'家的空气答案/产出/20261028_双重防漏_官方结构核验/官方视频原帧/10_泵浮子接水盘全貌_33点25秒.png'
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
enc=['-an','-r','30','-c:v','h264_videotoolbox','-b:v','14M','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart']
def clip(src,out,start,dur,vf=''):
 if out.exists() and out.stat().st_size>1000:return
 filt='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1'+(','+vf if vf else '')
 run(['-ss',start,'-i',src,'-t',dur,'-vf',filt,*enc,out])
items=[]
def add(idx,start,end,source,kind,detail):
 out=E/f'{idx:02}_{start:02}-{end:02}_{detail}.mp4';items.append({'id':idx,'start':start,'end':end,'duration':end-start,'file':str(out),'source':str(source),'kind':kind,'description':detail});return out
clip(A/'renovation.mp4',add(1,0,4,A/'renovation.mp4','Seedance2.0Fast720p','秋冬装修选材'),0,4)
opening=add(2,4,11,OLD,'官方片复用','漏水维修快切')
if not opening.exists() or opening.stat().st_size<1000:
 selected=[next(OLD.glob(f'{i:02}_*.mp4')) for i in [1,2,3,4,5,6,8]]
 lst=R/'edit/开头复用列表.txt';lst.write_text('\n'.join("file '"+str(x)+"'" for x in selected))
 run(['-f','concat','-safe','0','-i',lst,'-vf','setpts=(7/6.5)*PTS,fps=30,scale=1080:1920,setsar=1,eq=saturation=0.88:gamma=1.03','-t',7,*enc,opening])
clip(A/'vent.mp4',add(3,11,13,A/'vent.mp4','Seedance2.0Fast720p','推近线性风口'),2,2)
clip(A/'cup.mp4',add(4,13,15,A/'cup.mp4','Seedance2.0Fast720p','冰饮杯外凝露'),1,2)
for idx,st,en,shot,label in [(5,15,23,'condense','翅片凝水汇流'),(6,23,28,'overflow','通用接水盘溢水')]:
 out=add(idx,st,en,A/f'3D_{shot}.mp4','BlenderEEVEE',label)
 if (A/f'3D_{shot}.mp4').exists():clip(A/f'3D_{shot}.mp4',out,0,en-st)
clip(A/'renovation.mp4',add(7,28,32,A/'renovation.mp4','Seedance2.0Fast720p','防漏设计选材'),2,4)
hero=add(8,32,38,OFF,'官方CG原帧','官方泵浮子亮相')
if not hero.exists() or hero.stat().st_size<1000:
 run(['-loop',1,'-i',OFF,'-vf',"crop=608:1080:735:0,scale=2160:3840,zoompan=z='1+0.00017*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=180:s=1080x1920:fps=30,colorbalance=rs=.025:bs=-.018,setsar=1",'-frames:v',180,*enc,hero])
for idx,st,en,shot,label in [(9,38,44,'pump','提升泵主动排水'),(11,55,58,'protect','双重保护合拢')]:
 out=add(idx,st,en,A/f'3D_{shot}.mp4','BlenderEEVEE',label)
 if (A/f'3D_{shot}.mp4').exists():clip(A/f'3D_{shot}.mp4',out,0,en-st)
# Generic blower is a separate explanatory insert, not an invented installation location.
fl=add(10,44,55,A/'3D_float.mp4','BlenderEEVEE','异常水位停机保护')
if (A/'3D_fan.mp4').exists() and (not fl.exists() or fl.stat().st_size<1000):
 run(['-i',A/'3D_float.mp4','-i',A/'3D_fan.mp4','-filter_complex','[0:v]split=2[a][b];[a]trim=start=0:end=7.5,setpts=PTS-STARTPTS[x];[1:v]trim=start=0:end=2,setpts=PTS-STARTPTS[y];[b]trim=start=9.5:end=11,setpts=PTS-STARTPTS[z];[x][y][z]concat=n=3:v=1:a=0,setsar=1[v]','-map','[v]',*enc,fl])
clip(A/'vent.mp4',add(12,58,59,A/'vent.mp4','Seedance2.0Fast720p反向片段','完好吊顶回归'),3,1,'reverse')
clip(A/'house.mp4',add(13,59,65,A/'house.mp4','Seedance2.0Fast720p','安心家居收尾'),0,6)
items.sort(key=lambda x:x['start'])
(R/'edit/剪辑清单.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
missing=[x['file'] for x in items if not Path(x['file']).exists() or Path(x['file']).stat().st_size<1000]
if missing:print('等待3D段',missing);sys.exit(0)
lst=R/'edit/全片拼接列表.txt';lst.write_text('\n'.join("file '"+x['file']+"'" for x in items))
visual=R/'output/01_全片画面_无文字无声_65秒.mp4'
run(['-f','concat','-safe','0','-i',lst,'-c','copy','-movflags','+faststart',visual])
final=R/'output/CC_20261028_家的空气答案06_双重防漏_v1.mp4'
run(['-i',visual,'-i',A/'audio/成片混音_65秒.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-t',65,'-movflags','+faststart',final])
print('DONE',final)
