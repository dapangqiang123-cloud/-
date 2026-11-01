from pathlib import Path
import json, subprocess, sys

ROOT = Path(__file__).resolve().parent
OUT = ROOT / '剪映分镜'
OUT.mkdir(exist_ok=True)
BASE = Path('/Users/weipeilong/Desktop/璀璨中央空调/资料&客户提供/视频:达人素材/产品视频')
OFFICIAL = BASE / '11个卖点口播短视频/03.防漏水双重保护 男1-净版.mov'
INSTALL1 = BASE / '产品素材片段/工人安装出风口素材1.MP4'
INSTALL2 = BASE / '产品素材片段/工人安装出风口素材2.MP4'
# Crops are selected from inspected source frames. Source files remain untouched.
shots = [
    ('01_风口旁泡顶起皮', OFFICIAL, 7.00, 1.20, (608,1080,850,0), 0.035),
    ('02_吊顶水渍霉斑', OFFICIAL, 19.70, 0.75, (608,1080,650,0), 0.025),
    ('03_受损细节冲击', OFFICIAL, 21.00, 0.55, (540,960,1050,120), 0.055),
    ('04_拆装风口检修', INSTALL1, 1.20, 1.20, (1216,2160,1100,0), 0.015),
    ('05_风口操作特写', INSTALL2, 3.60, 0.85, (1000,1778,1580,0), 0.02),
    ('06_吊顶修复施工', OFFICIAL, 9.10, 0.95, (540,960,100,30), 0.02),
    ('07_受损墙面铲除', OFFICIAL, 12.90, 1.50, (608,1080,260,0), 0.035),
    ('08_泡顶后果落点', OFFICIAL, 21.40, 1.00, (608,1080,920,0), 0.025),
]

def run(args):
    subprocess.run(args, check=True)

ledger=[]
for i,(name,src,start,duration,crop,push) in enumerate(shots):
    frames=round(duration*60)
    w,h,x,y=crop
    vf=f'crop={w}:{h}:{x}:{y},fps=60,scale=1080:1920:flags=lanczos,setsar=1'
    vf+=f",zoompan=z='1+{push}*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=60"
    vf+=',eq=contrast=1.035:saturation=0.92:brightness=0.012'
    if i in (2,3,5):
        vf+=",gblur=sigma=4:steps=1:enable='lt(n,3)'"
    vf+=',format=yuv420p'
    dest=OUT/f'{name}.mp4'
    if len(sys.argv)==1 or str(i+1) in sys.argv[1:]:
        run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(start),'-i',str(src),'-map','0:v:0','-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','fast','-crf','17','-movflags','+faststart','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(dest)])
    ledger.append(dict(name=name,source=str(src),source_in=start,duration=duration,crop=list(crop),output=str(dest)))
    print('rendered',name,flush=True)

concat=ROOT/'concat.txt'
concat.write_text(''.join("file '"+str(OUT/f'{s[0]}.mp4')+"'\n" for s in shots))
run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(ROOT/'双重防漏_开头快切_无字无口播_8秒.mp4')])
(ROOT/'剪辑清单.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
print('Complete',sum(s[3] for s in shots),flush=True)
