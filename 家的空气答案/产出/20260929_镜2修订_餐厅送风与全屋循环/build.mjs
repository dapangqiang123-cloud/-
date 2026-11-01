import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const prev=path.resolve(root,'../20260929_第四期_浅咖无文字全套');
let design=await fs.readFile(path.join(prev,'DESIGN.md'),'utf8');
design+='\n## 镜2本轮修订\n仅修改镜2 A/B。风口放到餐厅上方；客厅在左、餐厅在右。淡白风幕从餐厅风口沿右向左方向送达客厅，随后房间内形成持续循环。两种气流同时保留。横长连续板条，无竖格栅。时长仍为6秒，无文字无数字，纯色背景与配色不变。循环为概念示意，不画作实际回风口或实测轨迹。\n';
await fs.writeFile(path.join(root,'DESIGN.md'),design);
for(const p of ['HyperFrames工程','4K成片','1080预览','预览图','制作文件/检查日志'])await fs.mkdir(path.join(root,p),{recursive:true});
const scenes=[];
for(const variant of ['A','B']){
 const key='镜2_'+variant,source=path.join(prev,'HyperFrames工程',key),dir=path.join(root,'HyperFrames工程',key);await fs.mkdir(dir,{recursive:true});
 let html=await fs.readFile(path.join(source,'index.html'),'utf8');
 const vent=variant==='A'?`<g id="vent" data-location="above-dining"><path d="M612 44L843 201V251L612 94Z" fill="#EEE4D8" stroke="#C2AC97" stroke-width="1.7"/><g stroke="#8D7765" stroke-width="3">${Array.from({length:4},(_,i)=>`<path d="M625 ${78+i*6}L825 ${214+i*6}"/>`).join('')}</g></g>`:`<g id="vent" data-location="above-dining"><path d="M546 119H820V164H546Z" fill="#EEE4D8" stroke="#C2AC97" stroke-width="1.5"/><g stroke="#8D7765" stroke-width="2.5">${Array.from({length:4},(_,i)=>`<path d="M556 ${132+i*6}H808"/>`).join('')}</g></g>`;
 html=html.replace(/<g stroke="#8D7765"[\s\S]*?<\/g>/,vent);
 const paths=[];
 for(let i=0;i<14;i++){
  const t=i/13;
  if(variant==='A'){
   const x=628+194*t,y=100+132*t,ex=184+184*t,ey=340+154*t;
   paths.push(`M${x.toFixed(2)} ${y.toFixed(2)}C${(x-105).toFixed(2)} ${(y+42).toFixed(2)} ${(ex+130).toFixed(2)} ${(ey-56).toFixed(2)} ${ex.toFixed(2)} ${ey.toFixed(2)}`);
  }else{
   const x=560+242*t,y=153,ex=150+178*t,ey=315+155*t;
   paths.push(`M${x.toFixed(2)} ${y}C${(x-38).toFixed(2)} 229 ${(ex+122).toFixed(2)} ${(ey-34).toFixed(2)} ${ex.toFixed(2)} ${ey.toFixed(2)}`);
  }
 }
 const loop=variant==='A'?'M728 192C581 207 344 236 222 321C135 396 278 491 431 485C620 477 824 390 787 303C770 247 754 209 728 192Z':'M705 182C506 180 308 188 183 272C84 367 252 492 440 493C649 505 796 452 795 348C794 267 769 201 705 182Z';
 const airflow=`<g id="airflow" data-direction="dining-to-living">${paths.map((d,i)=>`<path id="supply-${i}" class="supply-base" d="${d}" stroke="#FFFFFF" stroke-width="2.5" opacity=".48"/>`).join('')}<g id="supply-motion">${paths.map(d=>`<path class="supply-moving" d="${d}" stroke="#FFFFFF" stroke-width="4.2" stroke-dasharray="28 95" opacity=".86"/>`).join('')}</g></g><g id="circulation"><path id="circulation-base" d="${loop}" stroke="#FFFFFF" stroke-width="2.6" opacity=".38"/><path id="circulation-moving" d="${loop}" stroke="#FFFFFF" stroke-width="6" stroke-dasharray="52 118" opacity=".9"/></g>`;
 html=html.replace(/<g id="airflow">[\s\S]*?<\/g>/,airflow);
 const timeline=`<script>
const tl=gsap.timeline({paused:true});
tl.from('#architecture',{opacity:0,y:12,duration:.8,ease:'power3.out'},.15);
document.querySelectorAll('#architecture .trace').forEach(p=>{const n=p.getTotalLength();p.style.strokeDasharray=n;tl.from(p,{strokeDashoffset:n,duration:1.1,ease:'sine.inOut'},.5)});
tl.from('#airflow',{opacity:0,duration:.45,ease:'expo.out'},.65);
document.querySelectorAll('.supply-base').forEach((p,i)=>{const n=p.getTotalLength();p.style.strokeDasharray=n;tl.from(p,{strokeDashoffset:n,duration:1.1,ease:'sine.out'},.72+i*.013)});
tl.from('#supply-motion',{opacity:0,duration:.5,ease:'sine.out'},1.05);
tl.to('.supply-moving',{strokeDashoffset:-740,duration:4.85,ease:'none'},1.05);
tl.from('#circulation',{opacity:0,duration:.7,ease:'power2.out'},1.85);
const base=document.querySelector('#circulation-base'),n=base.getTotalLength();base.style.strokeDasharray=n;
tl.from(base,{strokeDashoffset:n,duration:1.25,ease:'sine.inOut'},1.9);
tl.from('#circulation-moving',{opacity:0,duration:.6,ease:'sine.out'},2.15);
tl.to('#circulation-moving',{strokeDashoffset:-765,duration:3.75,ease:'none'},2.15);
window.__timelines={main:tl};window.seek=t=>{tl.seek(t,false)};
</script>`;
 html=html.replace(/<script>[^]*?<\/script>/,timeline).replace(/<title>.*?<\/title>/,`<title>${key} 餐厅送风至客厅并全屋循环 修订版</title>`);
 await fs.writeFile(path.join(dir,'index.html'),html);await fs.copyFile(path.join(source,'gsap.min.js'),path.join(dir,'gsap.min.js'));await fs.copyFile(path.join(root,'DESIGN.md'),path.join(dir,'DESIGN.md'));
 scenes.push({key,id:2,variant,title:'餐厅送风至客厅 · 全屋循环',duration:6,dir,v4:path.join(root,'4K成片',key+'_餐厅送风循环_4K.mp4'),v1:path.join(root,'1080预览',key+'_餐厅送风循环_1080.mp4'),reused:false});
}
await fs.writeFile(path.join(root,'制作文件/scenes.json'),JSON.stringify(scenes,null,2));
const render=(await fs.readFile(path.join(prev,'render.mjs'),'utf8')).replace('tile=7x1','tile=6x1').replace('ALL SIX COMPLETE','BOTH REVISED SHOT 2 COMPLETE');
await fs.writeFile(path.join(root,'render.mjs'),render);
console.log('Two revised compositions prepared');
