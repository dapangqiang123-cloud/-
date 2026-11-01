from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'OpenFilm工程'
base='''<!doctype html><html><head><meta charset="UTF-8"><style>html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:transparent}.p{position:absolute;will-change:transform;box-shadow:0 0 34px #362A2220;background:#F0ECE1 url('assets/paper.jpg') center/1920px 1080px}</style></head><body>BODY<script>
const type=TYPE;const clamp=x=>Math.max(0,Math.min(1,x));const ease=x=>{x=clamp(x);return x*x*(3-2*x)};window.film={duration:.7,width:1920,height:1080,ready:Promise.all([...document.images].map(i=>i.decode())),frame(t){const p=ease(t/.7);CODE}};</script></body></html>'''
for i in range(1,6):
 if i==1:
  body=''.join(f'<div id="p{j}" class="p" style="left:0;top:{j*360}px;width:1920px;height:362px;overflow:hidden"><img src="assets/mountain.png" style="position:absolute;width:1500px;left:400px;top:{200-j*360}px;opacity:.5"/></div>' for j in range(3))
  code="for(let j=0;j<3;j++){let q=ease((t-j*.018)/(.7-j*.036));document.getElementById('p'+j).style.transform=`translateX(${(-1920+3840*q)}px)`;}"
 elif i==2:
  body=''.join(f'<div id="p{j}" class="p" style="left:{j*640}px;top:0;width:642px;height:1080px;overflow:hidden"><img src="assets/room.png" style="position:absolute;width:1920px;height:1080px;object-fit:cover;left:{-j*640}px;top:0"/></div>' for j in range(3))
  code="for(let j=0;j<3;j++){let q=ease(t/.7);document.getElementById('p'+j).style.transform=`translateY(${(-1080+2160*q)*(j%2?-1:1)}px)`;}"
 elif i==3:
  body='<div id="p0" class="p" style="left:0;top:-400px;width:2100px;height:1880px;transform-origin:center;overflow:hidden"><img src="assets/leaf.png" style="position:absolute;width:1400px;height:1400px;object-fit:contain;right:-400px;top:200px"/></div>'
  code="document.getElementById('p0').style.transform=`translateX(${-2700+5400*p}px) rotate(-17deg)`;"
 elif i==4:
  body='<div id="p0" class="p" style="left:0;top:0;width:1920px;height:540px"></div><div id="p1" class="p" style="left:0;top:540px;width:1920px;height:540px"></div>'
  code="document.getElementById('p0').style.transform=`translateX(${-1920+3840*p}px)`;document.getElementById('p1').style.transform=`translateX(${1920-3840*p}px)`;"
 else:
  body='<div id="p0" style="position:absolute;left:-200px;top:0;width:2320px;height:1080px;background:#3C302A;border-left:8px solid #BC936F;box-sizing:border-box"></div>'
  code="document.getElementById('p0').style.transform=`translateX(${2320*(1-2*p)}px)`;"
 (P/f'transition{i}.html').write_text(base.replace('BODY',body).replace('TYPE',str(i)).replace('CODE',code))
f=P/'film.html';s=f.read_text();track='<section id="transitions">'+''.join(f'<iframe id="transition-{i+1}" src="transition{i+1}.html#t=0,0.7" at="{round(t-.35,3)}"></iframe>' for i,t in enumerate([4.2,7.8,12,16.5,21.5]))+'</section>'
if 'id="transitions"' not in s:f.write_text(s.replace('<body>','<body>'+track))
print('Five cross-cut transitions installed')
