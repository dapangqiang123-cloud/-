from pathlib import Path
import math,random,json,shutil,re
root=Path.cwd(); old=root/'家的空气答案/产出/20261027_第六期_C3一拖多按需开_无字动画'
b=root/'家的空气答案/产出/20261028_第六期_C3一拖多_手绘有字版V2'; p=b/'HyperFrames工程'
p.mkdir(parents=True,exist_ok=True); (p/'assets').mkdir(exist_ok=True); (b/'检查').mkdir(exist_ok=True)
for name in ['AGENTS.md','CLAUDE.md','package.json','hyperframes.json']:
 shutil.copy2(old/'HyperFrames工程'/name,p/name)
shutil.copy2(old/'HyperFrames工程/assets/gsap.min.js',p/'assets/gsap.min.js')
design='''# C3一拖多｜手绘有字版 V2

## Style Prompt
按用户2026-10-28三项修改：外机直接参考清晰C3知境多联机W6C双风扇原始产品图，重画为暖咖铅笔线稿与浅色淡彩。保留竖向双风扇、香槟金风圈和右侧维修面板的比例。满幅使用可辨识的暖米杏底色，室内模块右侧加入客厅、主卧、次卧、书房。独立启停与原8秒节奏保持一致，下方留字幕空间。

## Colors
- 背景：#E5D2B8，满画幅暖米杏色，字幕留白区也有底色。
- 示意图底板：#F7EBD6，暖米纸色。
- 外机淡彩：#C2A89A；服务面板#B19B8E；墨线#765A4B。
- 风圈/管路：#B28A65，亮边#D4AF83。
- 标签：#5E4538；暖风：#FFF7E7。

## Typography
右侧房间名：宋体SC Medium，48px，深咖色；仅客厅、主卧、次卧、书房，不加温度或功能标题。

## Layout
1080×1920，8秒，30fps。沿用一拖四布局；主体y=300–1355；底部565px保持清楚的纯底色空白，可加后期字幕。室内风口只用吊顶横向叶片，无竖格栅。

## Motion
沿用四路依次启动、第2路关闭、第4路关闭后独立重启；风叶转动、管路线段与暖白风效持续运行。固定种子的线条与静态淡彩模拟手绘，清晰不抖动。

## What NOT to Do
- 不把产品照片直接贴进画面或磨糊为插画。
- 不做蓝/青冷风或竖格栅。
- 不添加温度、额外大标题或底部字幕。
- 不改变8秒原动作节奏。
'''
(p/'DESIGN.md').write_text(design); (b/'DESIGN.md').write_text(design)
rng=random.Random(1028)
def sketch_circle(cx,cy,r,stroke,width=2.2,opacity=1,fill='none',jitter=0.8):
 # A stable irregular outline, sampled once at authoring; no frame-to-frame noise.
 pts=[]
 for k in range(65):
  a=2*math.pi*k/64; rr=r+rng.uniform(-jitter,jitter)
  pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
 d='M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in pts)+' Z'
 return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}" stroke-linejoin="round"/>'
def fan(cx,cy,n):
 a=[sketch_circle(cx,cy,108,'#A17A55',3.1,1,'#DAC5AC',.55),sketch_circle(cx+.5,cy+.5,104,'#F5E7CF',2.6,.9,'none',.8),sketch_circle(cx,cy,99,'#876A55',1.8,.8,'#D6C0A8',.65),f'<g id="rotor{n}">']
 for k in range(7):
  a.append(f'<path d="M{cx-6} {cy-6} C{cx+15} {cy-80} {cx+70} {cy-86} {cx+78} {cy-42} C{cx+80} {cy-9} {cx+30} {cy+6} {cx+5} {cy+10} Z" transform="rotate({k*360/7:.3f} {cx} {cy})" fill="#9D7F6D" fill-opacity=".18" stroke="#9D7F6D" stroke-width="1.2" stroke-opacity=".45"/>')
 a.append('</g>')
 for r in [32,54,77,96]: a.append(sketch_circle(cx,cy,r,'#96765E',1.15,.55,jitter=.7))
 for k in range(28):
  t=k*2*math.pi/28; q=t+.42
  x1,y1=cx+20*math.cos(t),cy+20*math.sin(t)
  mx,my=cx+59*math.cos(t+.10),cy+59*math.sin(t+.10)
  x2,y2=cx+99*math.cos(q),cy+99*math.sin(q)
  a.append(f'<path d="M{x1:.2f} {y1:.2f} Q{mx:.2f} {my:.2f} {x2:.2f} {y2:.2f}" stroke="#8C6E58" fill="none" stroke-width="1.25" opacity=".63"/>')
 for k in range(44):
  t=k*2*math.pi/44
  x1,y1=cx+103*math.cos(t),cy+103*math.sin(t); x2,y2=cx+108*math.cos(t+.025),cy+108*math.sin(t+.025)
  a.append(f'<path d="M{x1:.2f} {y1:.2f} L{x2:.2f} {y2:.2f}" stroke="#AC845D" stroke-width="1.3" opacity=".7"/>')
 a.append(sketch_circle(cx,cy,21,'#9C7652',1.8,1,'#CFAC77',.65)); a.append(f'<path d="M{cx-10} {cy-12} Q{cx-1} {cy-20} {cx+11} {cy-12}" stroke="#F5E2B9" stroke-width="2" opacity=".7" fill="none"/>')
 return ''.join(a)
hatch=[]
for start in range(-430,440,15):
 x1=max(91,start); x2=min(435,start+520)
 y1=640+x1-start; y2=640+x2-start
 if x1<x2 and y1<=1160:
  hatch.append(f'<path d="M{x1} {y1} Q{(x1+x2)/2+.2:.1f} {(y1+y2)/2+.2:.1f} {x2} {y2}" fill="none" stroke="#856352" stroke-width=".85" opacity=".12"/>')
body='M96 636 Q252 633 430 636 Q438 636 438 645 L437 1157 Q438 1165 429 1165 L97 1164 Q88 1165 89 1155 L88 645 Q88 637 96 636 Z'
outdoor=f'''<g id="outdoor" stroke-linecap="round" stroke-linejoin="round">
<ellipse cx="262" cy="1187" rx="177" ry="14" fill="#94714F" opacity=".13"/>
<path d="M119 1163 L119 1175 L151 1176 L152 1165 M370 1164 L370 1176 L404 1175 L404 1165" fill="#B69A7F" stroke="#88674E" stroke-width="2.3"/>
<path d="{body}" fill="#C2A89A" fill-opacity=".73" stroke="#765A4B" stroke-width="3.4"/>
<path d="M94 640 Q267 637 433 640 L432 1159 Q264 1162 94 1159 Z" fill="none" stroke="#9E7E68" stroke-width="1.2" opacity=".6"/>
<path d="M333 640 Q383 639 433 641 L432 1160 L332 1160 Q335 896 333 640" fill="#B19B8E" fill-opacity=".35" stroke="#8A6C5A" stroke-width="1.65"/>
<g clip-path="url(#cabinetClip)">{''.join(hatch)}</g>
<path d="M96 649 Q253 646 429 650 M95 1152 Q256 1156 429 1153" fill="none" stroke="#E9D4B9" stroke-width="2.1" opacity=".7"/>
{fan(213,770,'A')}{fan(213,1024,'B')}
<path d="M345 821 Q382 823 421 821 M345 1014 Q383 1012 420 1014" stroke="#997763" stroke-width="1.3" fill="none"/>
<g fill="#8B6852"><circle cx="102" cy="650" r="2.6"/><circle cx="423" cy="650" r="2.6"/><circle cx="102" cy="1152" r="2.6"/><circle cx="423" cy="1152" r="2.6"/></g>
<path d="M350 690 Q378 689 404 690" fill="none" stroke="#9C7A59" stroke-width="2"/>
<path id="status" d="M351 689 L374 689" stroke="#FFF0CF" stroke-width="3.7" opacity="0"/>
<circle cx="438" cy="900" r="5.2" fill="#AB805A"/>
</g>'''
html=(old/'HyperFrames工程/index.html').read_text()
# Refine the existing scene in place, retaining the previously verified animation timing.
html=html.replace('璀璨C3一拖多按需开｜无字动画','璀璨C3一拖多按需开｜手绘有字V2')
html=html.replace('background:#F5F2ED','background:#E5D2B8').replace('fill="#F5F2ED"','fill="#E5D2B8"').replace('stop-color="#F5F2ED"','stop-color="#E5D2B8"')
html=html.replace('stop-color="#FFFDF6"','stop-color="#F4E4C9"')
html=html.replace('fill="#FCF8F1" fill-opacity=".48"','fill="#F7EBD6" fill-opacity=".7"')
html=html.replace('stroke="#C9AE92"','stroke="#BE9A76"').replace('stroke="#FFFCF6"','stroke="#F6E7CE"')
html=html.replace('.hot,.flow{mix-blend-mode:normal}', '@font-face{font-family:"RoomSongti";src:local("Songti SC Bold"),local("SongtiSC-Bold");font-weight:600;font-style:normal}.room-label{font-family:"RoomSongti",serif;font-size:48px;font-weight:600;fill:#5E4538;letter-spacing:2px;text-rendering:geometricPrecision}')
html=html.replace('id="ambient"','id="ambient" data-layout-allow-overflow="true"')
html=html.replace('<defs>','<defs><clipPath id="cabinetClip"><path d="'+body+'"/></clipPath>',1)
html=re.sub(r'<g id="outdoor">.*?(?=\n<g id="room1")',outdoor,html,flags=re.S)
html=html.replace('M414 900 H510','M438 900 H510')
for i,(y,label) in enumerate(zip([407,643,879,1115],['客厅','主卧','次卧','书房']),1):
 needle=f'<g id="switch{i}">'
 html=html.replace(needle,f'<text id="label{i}" class="room-label" x="905" y="{y+89}" text-anchor="middle">{label}</text>\n '+needle)
 # Soft double trace gives the panel a drawn outline, labels remain clean and readable.
 before=f'<rect id="warm{i}"'
 trace=f'<path d="M674 {y+4} Q816 {y+2} 978 {y+5} Q998 {y+7} 999 {y+26} L998 {y+144} Q997 {y+166} 978 {y+168} L675 {y+166}" fill="none" stroke="#C8AE8E" stroke-width="1" opacity=".33"/>'
 html=html.replace(before,trace+'\n '+before)
(p/'index.html').write_text(html)
(p/'meta.json').write_text(json.dumps({'name':'C3一拖多_手绘有字V2','width':1080,'height':1920,'duration':8,'updated':'2026-10-28'},ensure_ascii=False,indent=2))
meta=json.loads((old/'动画节奏.json').read_text()); meta.update({'text':True,'roomNames':['客厅','主卧','次卧','书房'],'style':'C3原始外形参考，暖咖铅笔淡彩，满幅暖米杏底色','generationsThisRevision':0})
(b/'动画节奏.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
# Retain the small authoring script for future geometry and label edits.
shutil.copy2('/tmp/air_c3_handdraw_v2.py',b/'重绘脚本.py')
print(b)
