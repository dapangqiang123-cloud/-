from pathlib import Path
import json,shutil
root=Path.cwd(); old=root/'家的空气答案/产出/20261028_第六期_C3一拖多_手绘有字版V2'; b=root/'家的空气答案/产出/20261028_第六期_C3一拖多_安全区逆时针V3'; p=b/'HyperFrames工程'
p.mkdir(parents=True,exist_ok=True); (p/'assets').mkdir(exist_ok=True); (b/'检查').mkdir(exist_ok=True)
for name in ['AGENTS.md','CLAUDE.md','package.json','hyperframes.json']:
 shutil.copy2(old/'HyperFrames工程'/name,p/name)
shutil.copy2(old/'HyperFrames工程/assets/gsap.min.js',p/'assets/gsap.min.js')
s=(old/'HyperFrames工程/DESIGN.md').read_text().replace('手绘有字版 V2','安全区与逆时针 V3').replace('宋体SC Medium','宋体SC Bold')
s=s.replace('沿用一拖四布局；主体y=300–1355；','一拖四布局左右收拢：外框x=120–960，左右各约120px安全边距；外机右移66px、四路内机左移66px，保持产品比例和48px字号；主体y=300–1355；')
s=s.replace('风叶转动、管路线段与暖白风效持续运行。','两个风扇从正面观看均逆时针转动（负角度），管路线段与暖白风效持续运行。')
(p/'DESIGN.md').write_text(s);(b/'DESIGN.md').write_text(s)
h=(old/'HyperFrames工程/index.html').read_text()
h=h.replace('手绘有字V2','安全区逆时针V3')
h=h.replace('<rect x="42" y="300" width="996"','<rect x="120" y="300" width="840"',1).replace('M85 321 H600','M150 321 H600',1)
h=h.replace('<g id="outdoor" stroke','<g id="outdoor-safe" transform="translate(66 0)"><g id="outdoor" stroke',1)
needle='</g>\n<g id="room1"'; assert h.count(needle)==1
h=h.replace(needle,'</g></g>\n<g id="rooms-safe" transform="translate(-66 0)"><g id="room1"',1)
h=h.replace('\n</svg>','\n</g></svg>',1)
h=h.replace('M438 900 H510','M504 900 H540').replace('H652"','H586"')
h=h.replace('rotation:1100','rotation:-1100').replace('rotation:1040','rotation:-1040')
assert 'rotation:1100' not in h and 'rotation:1040' not in h
(p/'index.html').write_text(h)
(p/'meta.json').write_text(json.dumps({'name':'C3一拖多_安全区逆时针V3','width':1080,'height':1920,'duration':8,'updated':'2026-10-28'},ensure_ascii=False,indent=2))
t=json.loads((old/'动画节奏.json').read_text());t.update({'horizontalSafeMarginsPx':[120,120],'outdoorTranslateX':66,'roomsTranslateX':-66,'fanDirectionFrontView':'counterclockwise','fanRotationDegrees':[-1100,-1040]})
(b/'动画节奏.json').write_text(json.dumps(t,ensure_ascii=False,indent=2));shutil.copy2('/tmp/air_c3_safe_v3.py',b/'修订脚本.py')
print(b)
