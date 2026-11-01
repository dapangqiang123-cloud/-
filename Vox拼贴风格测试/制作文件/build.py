from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'OpenFilm工程';P.mkdir(exist_ok=True)
css=r'''
@font-face{font-family:TresorSans;src:url('assets/body.woff2')}*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:transparent}body{font-family:TresorSans,'PingFang SC',sans-serif;color:#3F3028}#stage{position:relative;width:1920px;height:1080px;overflow:hidden;background:#F0ECE1 url('assets/paper.jpg') center/cover}.layer{position:absolute;transform-origin:50% 50%;will-change:transform}.photo{object-fit:contain}.serif{font-family:'Songti SC','STSong',Georgia,serif;font-weight:600}h1,h2,p{margin:0}h1{font-size:92px;line-height:1.22;letter-spacing:3px}h2{font-size:66px;line-height:1.35;letter-spacing:2px}.eyebrow{font-family:Georgia,serif;font-size:21px;letter-spacing:5px}.small{font-size:26px;letter-spacing:4px}.label{font-size:25px;letter-spacing:2px}.fine{font-size:20px;letter-spacing:3px}.brand{position:absolute;left:62px;top:45px;width:222px;height:88px;padding:12px 16px;background:#40312A;z-index:40}.brand img{width:190px;height:65px;object-fit:contain}.corner{position:absolute;right:66px;top:67px;font-size:18px;letter-spacing:3px;color:#82715D;z-index:40}.rule{height:2px;background:#B59170;transform-origin:0 50%}.paper{background:#E5DDCE;box-shadow:0 11px 22px #45392A12}.disc{border-radius:50%;border:1px solid #B99B77}.ribbed{background:repeating-linear-gradient(90deg,#BAAA91 0px,#BAAA91 7px,#DFD3BD 8px,#DFD3BD 15px);border-top:10px solid #E2D7C4;box-shadow:0 15px 25px #493B2918}.route{fill:none;stroke:#F5F2E9;stroke-width:5;stroke-linecap:round;stroke-dasharray:12 10}.topo{opacity:.16;fill:none;stroke:#AA9476;stroke-width:1.5}.caption{font-size:40px;letter-spacing:5px}.window{background:#E9E2D4;border:16px solid #D5C3AA;border-bottom:28px solid #C8AF8C;border-radius:270px 270px 0 0;box-shadow:17px 17px 0 #B69B7618;overflow:hidden}.window:after{content:'';position:absolute;left:49.5%;top:0;width:10px;height:100%;background:#C8AF8C;box-shadow:3px 0 2px #FFFFFF55}.scene-no{position:absolute;right:65px;bottom:40px;font:20px Georgia;color:#8C7860;letter-spacing:3px}#sweep{pointer-events:none;z-index:80;left:0;top:0;width:1920px;height:1080px}#sweep img{position:absolute;width:1600px;height:1600px;object-fit:contain;left:150px;top:-220px;filter:drop-shadow(10px 15px 15px #4F442C22)}
'''
(P/'style.css').write_text(css+'.ribbed:before{content:"";position:absolute;left:-1px;top:-60px;width:calc(100% + 2px);height:112px;border-radius:50%;background:#DCCDB6;border:1px solid #C6B397;box-shadow:inset 0 -10px 16px #B8A18433}#product4,#product6{filter:drop-shadow(5px 12px 8px #33291D25)}')
js=r'''
const D=[4.2,3.6,4.2,4.5,5,3.5];const scene=Number(document.body.dataset.scene);const dur=D[scene-1];const stage=document.getElementById('stage');
const pic=(id,name,x,y,w,h,extra='')=>`<img id="${id}" class="layer photo" src="assets/${name}.png" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;${extra}"/>`;
const div=(id,cls,x,y,w,h,txt='',extra='')=>`<div id="${id}" class="layer ${cls}" style="left:${x}px;top:${y}px;${w?'width:'+w+'px;':''}${h?'height:'+h+'px;':''}${extra}">${txt}</div>`;
const topo=`<svg class="layer topo" width="1920" height="1080" viewBox="0 0 1920 1080"><path d="M-120 360C120 80 380 120 550 370S960 620 1130 300 1700 0 2050 350M-110 400C130 120 370 150 535 400S950 660 1150 330 1720 30 2050 390M-120 440C110 170 360 190 525 440S950 710 1170 370 1740 70 2050 430M-110 480C100 210 350 230 510 480S940 760 1190 410 1750 110 2050 470M-120 520C90 250 340 270 495 520S930 810 1210 450 1770 150 2050 510M-120 560C90 290 325 310 480 560S920 860 1230 490 1780 190 2050 550"/></svg>`;
const route=(id,path,color='#F4F0E5',width=5)=>`<svg class="layer" width="1920" height="1080" style="left:0;top:0;pointer-events:none"><path id="${id}" d="${path}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round"/></svg>`;
let s='';
if(scene===1){
 s=topo+div('label','eyebrow',105,225,700,40,'THE ART OF FRESH AIR')+div('title','serif',100,310,1000,260,'<h1>家的好风景，<br>只在眼前吗？</h1>')+div('line','rule',108,626,580,2)+div('intro','small',108,664,700,50,'让空气，也有风景')+
 div('portal','window',1110,190,600,720,pic('mountA','mountain',-145,115,980,540)+pic('forestA','forest',-60,440,750,370))+pic('leafA','leaf',800,680,280,320)+div('tiny','fine',1130,947,650,35,'A DIFFERENT KIND OF SCENERY');
}
if(scene===2){
 s=topo+div('head2','serif',300,190,1320,150,'<h1 style="text-align:center">让清新，翻山越岭</h1>')+pic('back2','mountain',530,355,1400,620,'filter:saturate(.8);')+pic('mid2','mountain',-280,450,1550,690)+pic('front2','forest',680,670,1450,640)+pic('frontL2','forest',-430,790,1200,520)+route('path2','M-80 970C220 750 260 1000 540 790S860 530 1050 725 1310 820 1540 665 1840 760 2050 460')+div('pin2','',1375,600,130,90,'<svg width="42" height="55" viewBox="0 0 42 55"><path fill="#BC936F" d="M21 0C-4 0-4 30 21 55C46 30 46 0 21 0"/><circle cx="21" cy="20" r="7" fill="#F5F0E3"/></svg><span style="position:absolute;left:54px;top:9px;font-size:27px;color:#fff">清新</span>')+pic('leaf2','leaf',0,0,130,150);
}
if(scene===3){
 s=topo+pic('nature3','forest',-330,765,1120,510)+div('room3','paper',755,190,1100,810,`<img src="assets/room.png" style="width:100%;height:100%;object-fit:cover;object-position:65% 50%"/>`,'clip-path:polygon(0 3%,38% 0,65% 2%,100% 0,99% 99%,61% 100%,28% 98%,0 100%);')+div('slat31','paper',755,190,15,810)+div('slat32','paper',1118,190,15,810)+div('slat33','paper',1485,190,15,810)+div('head3','serif',105,232,610,240,'<h1 style="font-size:82px">不开窗，<br>也能换口<br>新鲜空气</h1>')+div('sub3','small',110,605,580,50,'新风入室 · 浊气排出')+route('path3','M-50 860C250 720 480 950 695 760S1000 400 1180 550 1520 720 1960 470','#B78F69',5)+pic('leaf3','leaf',0,0,135,160);
}
if(scene===4){
 s=topo+div('halo4','disc',790,150,930,930,'','border-color:#BC9C7066;')+div('halo42','disc',885,245,740,740,'','border-color:#BC9C7044;')+div('head4','',105,260,700,450,'<p class="eyebrow">TRESOR AIR SYSTEM</p><h1 class="serif" style="font-size:138px;margin-top:27px">Mini</h1><h2 class="serif" style="margin-top:8px">全热交换新风系统</h2><p class="small" style="margin-top:47px">三层过滤 · 新鲜入室</p>')+div('plinth4','ribbed',990,935,720,145)+pic('product4','mini',810,285,1040,660)+pic('forest4','forest',-320,855,1140,500)+route('flow4a','M780 330C1050 110 1570 115 1780 350','#9FAD88',3)+route('flow4b','M1840 680C1690 950 1030 980 860 750','#B58E69',3)+div('flowLabel4','label',1230,180,440,40,'让家，自在呼吸')+pic('leaf4','leaf',1720,100,140,170);
}
if(scene===5){
 s=topo+pic('back5','mountain',690,285,1350,580,'opacity:.87;')+div('arch5','window',1250,230,400,660,`<img src="assets/room.png" style="width:100%;height:100%;object-fit:cover;object-position:right;"/>`)+pic('forest5','forest',820,655,1390,580)+div('ground5','',170,865,1000,85,'','border-radius:50%;background:#B6A58533;')+pic('chair5','chair',185,365,1000,650)+pic('leaf5','leaf',1520,330,180,200)+div('head5','serif',140,190,1100,140,'<h1>让生活，慢下来</h1>')+div('sub5','small',148,320,900,40,'每一次回家，都有好风景','font-size:27px;');
}
if(scene===6){
 s=div('dark6','',0,0,1920,1080,'','background:#3C302A')+pic('mount6','mountain',650,600,1450,640,'opacity:.65;filter:saturate(.55);')+pic('forest6','forest',1120,815,1100,470,'filter:saturate(.7);')+div('ring6','disc',1000,190,710,710,'','border:1px solid #BD9B6F77')+div('plinth6','ribbed',1070,960,650,120)+pic('product6','mini',940,390,850,570)+pic('logo6','logo',133,220,540,210)+div('head6','serif',132,555,850,240,'<h1 style="color:#F3EBDD;font-size:83px">理想空气，<br>源自璀璨。</h1>')+div('sub6','small',139,862,780,60,'璀璨 Mini 全热交换新风系统','color:#CFB597;font-size:28px;')+div('gold6','rule',140,806,650,2,'','background:#BC936F');
}
stage.innerHTML=s+(scene===6?'':`<div class="brand"><img src="assets/logo.png"/></div><div class="corner">让空气，也有风景</div>`);
// A leaf passes very close to the lens to carry the photographic cut between scenes.

const E=id=>document.getElementById(id);const clamp=x=>Math.max(0,Math.min(1,x));const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};const out=x=>1-Math.pow(1-clamp(x),3);const mix=(a,b,x)=>a+(b-a)*x;
function tr(id,x=0,y=0,scale=1,rot=0,alpha=1){const el=E(id);if(!el)return;el.style.transform=`translate(${x}px,${y}px) rotate(${rot}deg) scale(${scale})`;el.style.opacity=alpha}
function enter(id,t,start,len,dx=0,dy=50,sc=.98,rot=0){const v=out((t-start)/len);tr(id,dx*(1-v),dy*(1-v),mix(sc,1,v),rot*(1-v),v)}
function path(id,p){const e=E(id);let l=e.getTotalLength();e.style.strokeDasharray='12 10';e.style.strokeDashoffset=-p*120;e.style.clipPath=`inset(0 ${100*(1-clamp(p))}% 0 0)`;}
function leafOn(id,pathId,p,base=1){const e=E(pathId);let q=e.getPointAtLength(e.getTotalLength()*clamp(p));tr(id,q.x-65,q.y-70,base,Math.sin(p*9)*20);}
function frame(t){
 t += scene===1 ? .9 : .42;
 if(scene===1){
  enter('label',t,.1,.6,0,20,1);enter('title',t,.16,.85,0,55,1);enter('line',t,.35,.7,-25,0,.7);enter('intro',t,.55,.7,0,28,1);enter('portal',t,.12,1,230,30,.85,-4);enter('tiny',t,.9,.6,0,20,1);
  tr('mountA',-28*t,20-5*t,1.1);tr('forestA',-48*t,12*Math.sin(t),1.08);tr('leafA',120*Math.sin(t*.8),-60*Math.sin(t*.7),.8+ .06*Math.sin(t),-30+20*t,out(t/.8));
 }
 if(scene===2){
  enter('head2',t,.06,.72,0,45,1);tr('back2',-35*t,140*(1-out(t/.9)),1);tr('mid2',-70*t,200*(1-out(t/.7)),1.05);tr('front2',-115*t,230*(1-out(t/.65)),1);tr('frontL2',-145*t,180*(1-out(t/.55)),1);
  path('path2',out((t-.55)/2.5));enter('pin2',t,1.65,.5,0,-50,.8);leafOn('leaf2','path2',smooth(t/3.6),.8);
 }
 if(scene===3){
  enter('room3',t,.05,1.0,350,0,1,3);tr('nature3',-35*t,140*(1-out(t/.75)),1);enter('head3',t,.18,.8,-55,0,1);enter('sub3',t,.65,.7,-35,0,1);
  tr('slat31',-90*out(t/.9),0,1,0,1-out((t-.6)/.5));tr('slat32',110*out(t/.9),0,1,0,1-out((t-.6)/.5));tr('slat33',240*out(t/.9),0,1,0,1-out((t-.6)/.5));
  path('path3',out((t-.6)/2.4));leafOn('leaf3','path3',smooth((t-.7)/3.2),.9);
 }
 if(scene===4){
  enter('head4',t,.16,.85,-70,0,1);enter('plinth4',t,.05,.9,0,200,1);tr('product4',110*(1-out((t-.1)/1.1)),50*(1-out((t-.1)/1.1))-9*Math.sin(t),1,0,out((t-.1)/.55));enter('forest4',t,.1,1,-160,50,1);enter('halo4',t,.1,1,0,0,.85);enter('halo42',t,.3,1,0,0,.9);path('flow4a',out((t-.8)/1.3));path('flow4b',out((t-1.2)/1.6));enter('flowLabel4',t,1.3,.6,0,20,1);tr('leaf4',-35*t,35*Math.sin(t),.8,-25+17*t,out(t/.6));
 }
 if(scene===5){
  enter('head5',t,.1,.8,0,45,1);tr('back5',-16*t,110*(1-out(t/1)),1);enter('arch5',t,.2,1.1,150,0,.9);tr('forest5',-35*t,150*(1-out(t/.9)),1);enter('ground5',t,.25,.9,0,70,.8);enter('chair5',t,.1,1.1,-190,90,.93,-2);tr('leaf5',-68*t,90*Math.sin(t*.6),.8,30-18*t,out(t/.7));enter('sub5',t,1.15,.8,60,0,1);
 }
 if(scene===6){
  enter('logo6',t,.15,.7,0,30,1);enter('head6',t,.32,.85,0,45,1);enter('sub6',t,.65,.65,0,25,1);enter('gold6',t,.5,.8,-20,0,.7);enter('ring6',t,.1,1,0,0,.9);enter('plinth6',t,.08,.8,0,120,1);enter('product6',t,.12,.9,100,0,1);tr('mount6',-10*t,80*(1-out(t/.8)),1,0,.65);tr('forest6',-18*t,120*(1-out(t/.8)),1);
 }
 if(scene<6){const u=smooth((t-(dur-.42))/.42);tr('sweep',mix(-2600,2800,u),80*Math.sin(u*Math.PI),1.9,-50+u*95, u>0?1:0);}
}
window.film={duration:dur,width:1920,height:1080,ready:Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))).then(()=>document.fonts.ready),frame};
'''
(P/'scene.js').write_text(js)
for i in range(1,7):
 (P/f'scene{i}.html').write_text(f'<!doctype html><html lang="zh"><head><meta charset="UTF-8"><link rel="stylesheet" href="style.css"></head><body data-scene="{i}"><div id="stage"></div><script src="scene.js"></script></body></html>')
starts=[0,4.2,7.8,12,16.5,21.5];durs=[4.2,3.6,4.2,4.5,5,3.5]
clips='\n'.join(f'<iframe id="shot-{i+1}" title="{name}" src="scene{i+1}.html#t=0,{d}" at="{t}"></iframe>' for i,(t,d,name) in enumerate(zip(starts,durs,['眼前的风景','翻山越岭','不开窗换新风','Mini主角','自在日常','璀璨落版'])))
(P/'film.html').write_text(f'<!doctype html><html lang="zh"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080"><title>璀璨｜让空气，也有风景</title></head><body><section id="visuals">{clips}</section></body></html>')
print(P)
