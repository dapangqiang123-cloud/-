const n=+document.body.dataset.scene,D=+document.body.dataset.duration,stage=document.querySelector('#stage');
const clamp=x=>Math.max(0,Math.min(1,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x)},out=x=>1-Math.pow(1-clamp(x),3);
function el(id,cls,x,y,w,h,content){let e=document.createElement('div');e.id=id;e.className='el '+cls;Object.assign(e.style,{left:x+'px',top:y+'px',width:w+'px',height:h+'px'});e.innerHTML=content;stage.append(e);return e}
function img(id,file,x,y,w,h,cls=''){let e=document.createElement('img');e.id=id;e.className='el photo '+cls;e.src='assets/'+file;Object.assign(e.style,{left:x+'px',top:y+'px',width:w+'px',height:h+'px'});stage.append(e);return e}
function txt(id,text,x,y,w,size,cls='title'){let e=el(id,cls,x,y,w,300,text);e.style.fontSize=size+'px';return e}
function set(id,x=0,y=0,r=0,s=1,a=1){let e=document.getElementById(id);if(e){e.style.transform=`translate(${x}px,${y}px) rotate(${r}deg) scale(${s})`;e.style.opacity=a}}
let paths=[];function svg(mark){let box=document.createElement('div');box.innerHTML='<svg class="diagram" viewBox="0 0 1080 1920">'+mark+'</svg>';stage.append(box.firstChild)}
function path(id,d,color='#9b7551',width=7){paths.push(id);return `<path id="${id}" d="${d}" class="pencil" style="stroke:${color};stroke-width:${width}"/><path d="${d}" class="pencil echo" style="stroke:${color}" transform="translate(3 -3)"/>`}
function draw(id,p){let e=document.getElementById(id);if(!e)return;let l=e.getTotalLength();e.style.strokeDasharray=l;e.style.strokeDashoffset=l*(1-clamp(p))}
function dots(id,count,color){return Array.from({length:count},(_,i)=>`<g id="${id}${i}"><path d="M -14 -7 L 8 0 L -14 7" fill="none" stroke="${color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>`).join('')}
function travel(pathId,id,count,t,speed=.18,visible=1){let e=document.getElementById(pathId);let l=e.getTotalLength();for(let i=0;i<count;i++){let q=((t*speed+i/count)%1+1)%1;let p=e.getPointAtLength(l*q),p2=e.getPointAtLength(Math.min(l,l*q+3));let a=Math.atan2(p2.y-p.y,p2.x-p.x)*180/Math.PI;let g=document.getElementById(id+i);g.setAttribute('transform',`translate(${p.x} ${p.y}) rotate(${a})`);g.style.opacity=visible}}
img('logo','logo.png',76,82,245,100,'logo');el('series','kicker',650,113,350,55,'璀璨 · 空气小知识');
if(n===1){
 txt('title','空调开着，<br>就在换气？',76,290,950,108);
 img('room','room.png',10,660,1060,1000);
 txt('question','?',750,570,200,235,'handwriting');
 img('hand','hand.png',610,790,700,370);
 el('bottom','caption',80,1680,900,90,'先分清：空气变凉，还是空气换新。');
 svg(path('underline','M 77 557 Q 440 576 833 550')+path('circle','M 862 583 C 1020 584 1022 831 873 835 C 720 842 706 579 862 583','#b38f66',4));
}else if(n===2){
 txt('title','空气，<br>在室内转了一圈',76,285,950,91);
 el('note','small',80,544,930,70,'普通空调 · 不含独立新风功能');
 img('room','room.png',-50,665,1180,1040);
 el('tag','stamp',315,1510,450,100,'循环调温').style.fontSize='44px';
 txt('contrast','变凉 ≠ 换新',95,1720,920,86,'handwriting');
 svg(path('loop','M 280 905 C 420 845 704 857 815 975 C 929 1116 810 1358 559 1377 C 304 1391 164 1164 280 905','#9b7551',7)+dots('d',6,'#9b7551'));
}else if(n===3){
 el('outside','',0,580,190,930,'').style.background='#e1e4d8';
 txt('title','换新风，<br>要跨过这面墙',76,285,950,96);
 img('room','room.png',160,650,1030,1000);
 el('boundary','',188,630,2,880,'').style.borderLeft='2px dashed #aa947b';
 el('outlabel','sans',42,710,120,140,'室<br>外').style.fontSize='38px';
 el('inlabel','sans',600,710,300,90,'室内').style.fontSize='38px';
 el('incoming','stamp',270,1425,660,100,'室外空气送入').style.fontSize='42px';
 el('exiting','caption',270,1660,760,60,'室内空气排出');
 el('note','small',76,1780,920,90,'气流示意 · 非实际安装管路');
 svg(path('in','M 30 1000 C 210 1000 285 1000 490 1030 C 605 1043 697 1070 759 1100','#6d7c58',8)+path('out','M 760 1260 C 545 1270 389 1230 255 1230 L 32 1230','#a1846b',7)+dots('inDot',5,'#6d7c58')+dots('outDot',4,'#a1846b'));
}else if(n===4){
 txt('title','两件事。<br>各有分工。',76,280,950,100);
 img('ac','room.png',70,560,640,520);
 img('mini','mini.png',390,1130,590,440);
 el('cool','stamp',590,775,360,110,'管冷暖').style.fontSize='50px';
 el('fresh','stamp',85,1280,370,110,'管换气').style.fontSize='50px';
 el('acl','small',76,1105,550,60,'空调 · 循环调温');
 el('freshl','small',450,1605,570,60,'新风 · 室内外换气');
 svg(path('divider','M 86 1184 Q 512 1162 986 1190','#b49b7f',3)+path('snow','M 313 681 L 313 818 M 249 710 L 378 784 M 250 783 L 378 708','#9b7551',6)+path('newair','M 476 1501 C 571 1545 779 1552 903 1470','#6d7c58',5)+dots('air',3,'#6d7c58'));
 txt('footer','冷暖之外，别忘了换气。',80,1735,930,42,'sans');
}else{
 document.body.classList.add('dark');
 document.getElementById('logo').style.left='76px';document.getElementById('logo').style.top='110px';
 document.getElementById('series').remove();
 txt('title','让家，<br>自在呼吸。',76,400,930,116);
 el('name','sans',80,755,950,150,'璀璨 Mini<br>全热交换新风系统').style.fontSize='43px';
 el('paper','',-80,1110,1240,555,'').style.cssText+=';background:#e4d7c2;transform:rotate(-5deg);clip-path:polygon(1% 2%,98% 0,100% 97%,0 100%)';
 img('mini','mini.png',95,1025,890,650);
 el('end','sans',80,1790,930,80,'理想空气，源自璀璨。').style.fontSize='37px';
 svg(path('orbit','M 115 1190 C -50 1410 255 1683 705 1620 C 910 1590 1031 1430 949 1232','#b29470',5)+dots('d',5,'#b29470'));
}
window.film={width:1080,height:1920,duration:D,ready:Promise.all([...document.images].map(x=>x.decode()).concat([document.fonts.load('400 44px Body'),document.fonts.ready])),frame(t){
 const a=out((t+.2)/.6),k=Math.floor(t*12)/12;
 set('title',0,(1-a)*55,0,1,1);set('logo',0,0,0,1,1);
 if(n===1){set('room',0,30*(1-a),-1+.3*Math.sin(t),.95+.04*out(t/2));set('hand',150*(1-out((t-.25)/.7)),Math.sin(t*2)*7,-4,1,clamp((t-.1)*4));set('question',0,-15*Math.sin(t*2),-8,1,1);draw('underline',(t+.1)/.6);draw('circle',(t-.4)/.7);set('bottom',0,0,0,1,clamp((t-.8)*3));}
 if(n===2){set('room',0,0,0,1+.015*t);draw('loop',(t+.05)/.7);travel('loop','d',6,t,.18,clamp((t+.1)*2));set('tag',0,20*(1-a),-3,1,1);set('contrast',0,0,-2,1,clamp((t-1)*3));}
 if(n===3){set('room',-20*out(t/2),0,0,1);draw('in',(t+.1)/.55);draw('out',(t-.25)/.6);travel('in','inDot',5,t,.34,clamp((t+.1)*3));travel('out','outDot',4,t,.28,clamp((t-.2)*3));set('incoming',0,0,-2,1,clamp((t-.3)*3));set('exiting',0,0,0,1,clamp((t-.6)*3));}
 if(n===4){set('ac',-100*(1-a),0,-3,1,1);set('mini',100*(1-a),0,3,1,1);set('cool',0,0,-4,1,1);set('fresh',0,0,3,1,1);draw('divider',(t+.1)/.4);draw('snow',(t+.2)/.7);draw('newair',(t-.1)/.6);travel('newair','air',3,t,.3,1);}
 if(n===5){set('mini',0,55*(1-a),-2,1+.015*smooth(t/4),1);set('paper',0,0,-5,1,1);draw('orbit',(t+.3)/1.3);travel('orbit','d',5,t,.11,clamp(t*2));set('name',0,0,0,1,clamp((t+.2)*2));set('end',0,0,0,1,clamp((t-.6)*2));}
}};
if(!window.filmHost){const st=performance.now();Promise.resolve(window.film.ready).then(()=>{function tick(){window.film.frame(((performance.now()-st)/1000)%D);requestAnimationFrame(tick)}tick()})}
