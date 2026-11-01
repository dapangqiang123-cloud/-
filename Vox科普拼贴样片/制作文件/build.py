from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'OpenFilm工程';P.mkdir(exist_ok=True)
dur=[3,4,4,4,5];starts=[0,3,7,11,15]
for i,d in enumerate(dur,1):
 (P/f'scene{i}.html').write_text(f'<!doctype html><html><head><meta charset="UTF-8"><link rel="stylesheet" href="style.css"></head><body data-scene="{i}" data-duration="{d}"><main id="stage"></main><script src="scene.js"></script></body></html>')
f='<!doctype html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920"></head><body>'
f+='<section id="paper-transitions">'+''.join(f'<iframe id="paper-{i}" src="transition{i}.html#t=0,0.48" at="{t-.24}"></iframe>' for i,t in enumerate(starts[1:],1))+'</section>'
f+='<section id="pictures">'+''.join(f'<iframe id="shot-{i}" src="scene{i}.html#t=0,{d}" at="{at}"></iframe>' for i,(d,at) in enumerate(zip(dur,starts),1))+'</section></body></html>'
(P/'film.html').write_text(f)
for i in range(1,5):
 color='#3F3028' if i==4 else '#E8DECE';direction=-1 if i%2 else 1
 (P/f'transition{i}.html').write_text('''<!doctype html><html><head><style>html,body{margin:0;width:1080px;height:1920px;overflow:hidden}#paper{position:absolute;left:-120px;top:-120px;width:1320px;height:2160px;background:COLOR;clip-path:polygon(2% 0,99% 0,100% 13%,99% 29%,100% 51%,99% 76%,100% 100%,0 100%,1% 70%,0 41%,1% 19%);box-shadow:0 0 50px #30251a33}</style></head><body><div id="paper"></div><script>window.film={width:1080,height:1920,duration:.48,frame(t){let p=Math.min(1,Math.max(0,t/.48));p=p*p*(3-2*p);document.querySelector('#paper').style.transform=`translateX(${DIR*(1-2*p)*1440}px) rotate(2deg)`;}};</script></body></html>'''.replace('COLOR',color).replace('DIR',str(direction)))
print('Five-shot film created')
