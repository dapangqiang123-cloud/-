import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath,pathToFileURL} from 'node:url';import {chromium} from 'playwright';import sharp from 'sharp';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const b=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto(pathToFileURL(path.join(root,'HyperFrames工程/index.html')).href);
const frames=[],states=[];
for(const [t,name] of [[1.6,'四个机位'],[2.55,'减少中_三个'],[2.92,'减少中_两个'],[5.4,'一个机位']]){
 await p.evaluate(t=>{window.seek(t)},t);
 const f=path.join(root,'静帧',name+'.png');await p.screenshot({path:f});frames.push(await sharp(f).resize(270,480).toBuffer());
 states.push(await p.evaluate(t=>({time:t,units:[...document.querySelectorAll('.machine')].map(e=>({id:e.id,opacity:Number(getComputedStyle(e).opacity)})),text:document.body.innerText}),t));
}
await sharp({create:{width:1080,height:480,channels:3,background:'#faf7f0'}}).composite(frames.map((input,i)=>({input,left:i*270,top:0}))).png().toFile(path.join(root,'静帧/过程总览.png'));
await p.evaluate(()=>{window.seek(5.4);window.setTransparent(true)});await p.screenshot({path:path.join(root,'静帧/一个机位_透明.png'),omitBackground:true});
const tweens=await p.evaluate(()=>window.__timelines.main.getChildren(false,true,false).map(t=>({start:t.startTime(),end:t.endTime(),targets:t.targets().map(e=>e.id||e.className?.baseVal||e.className),properties:Object.keys(t.vars).filter(k=>!['parent','duration','ease','stagger'].includes(k))})));
await fs.writeFile(path.join(root,'制作文件/动画时序与机位数量检查.json'),JSON.stringify({states,tweens,method:'GSAP inspection and sampled screenshots'},null,2));
if(states[0].units.filter(u=>u.opacity>.99).length!==4||states.at(-1).units.filter(u=>u.opacity>.99).length!==1||states.some(s=>s.text.trim()))throw Error('Unit count / no-text assertion failed');
await b.close();console.log('4 → 1 checked; no text; snapshots exported');
