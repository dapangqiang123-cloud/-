import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath,pathToFileURL} from 'node:url';import {chromium} from 'playwright';import sharp from 'sharp';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const b=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
try{
const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto(pathToFileURL(path.join(root,'HyperFrames工程/index.html')).href);
const structure=await p.evaluate(()=>({singles:[...document.querySelectorAll('.single')].map(e=>e.querySelectorAll('.fan-rim').length),doubles:[...document.querySelectorAll('.double')].map(e=>e.querySelectorAll('.fan-rim').length),gradients:document.querySelectorAll('linearGradient,radialGradient,filter').length,text:document.body.innerText}));
if(structure.singles.length!==4||structure.singles.some(n=>n!==1)||structure.doubles.length!==1||structure.doubles[0]!==2||structure.gradients||structure.text.trim())throw Error('Geometry / no-text check failed');
const frames=[],states=[];
for(const [t,name,n,d] of [[1.5,'01_四台单风扇',4,0],[2.16,'02_剩三台单风扇',3,0],[2.64,'03_剩两台单风扇',2,0],[3.12,'04_剩一台单风扇',1,0],[3.6,'05_四台已全部退出',0,0],[5.4,'06_一台双风扇替代',0,1]]){
 await p.evaluate(t=>{window.seek(t)},t);
 const state=await p.evaluate(t=>({time:t,units:[...document.querySelectorAll('.machine')].map(e=>({id:e.id,type:e.classList.contains('single')?'single':'double',opacity:Number(getComputedStyle(e).opacity)}))}),t);
 if(state.units.filter(u=>u.type==='single'&&u.opacity>.001).length!==n||state.units.filter(u=>u.type==='double'&&u.opacity>.001).length!==d)throw Error('Wrong replacement state at '+t);
 states.push(state);const f=path.join(root,'静帧',name+'.png');await p.screenshot({path:f});frames.push(await sharp(f).resize(324,576).toBuffer());
 const flat=await sharp(await sharp(f).extract({left:0,top:0,width:1080,height:400}).toBuffer()).stats();if(flat.channels.some(c=>c.min!==c.max))throw Error('Background not uniform');
}
await sharp({create:{width:972,height:1152,channels:3,background:'#e9dfd2'}}).composite(frames.map((input,i)=>({input,left:i%3*324,top:Math.floor(i/3)*576}))).png().toFile(path.join(root,'静帧/六阶段过程总览.png'));
// Check every frame, including partially visible exits: old and new units must never coexist.
const audit=await p.evaluate(()=>{const overlaps=[];for(let i=0;i<360;i++){window.seek(i/60);const old=[...document.querySelectorAll('.single')].some(e=>Number(getComputedStyle(e).opacity)>.001);const fresh=Number(getComputedStyle(document.querySelector('.double')).opacity)>.001;if(old&&fresh)overlaps.push(i)}return {checkedFrames:360,overlapFrames:overlaps}});
if(audit.overlapFrames.length)throw Error('Old and new machines overlap');
await p.evaluate(()=>{window.seek(5.4);window.setTransparent(true)});await p.screenshot({path:path.join(root,'静帧/尾帧_透明.png'),omitBackground:true});
const tweens=await p.evaluate(()=>window.__timelines.main.getChildren(false,true,false).map(t=>({start:t.startTime(),end:t.endTime(),targets:t.targets().map(e=>e.id||e.className?.baseVal||e.className)})));
await fs.writeFile(path.join(root,'制作文件/替代逻辑与动画时序检查.json'),JSON.stringify({structure,states,audit,tweens},null,2));
console.log('Verified 4 single → 3 → 2 → 1 → 0 → 1 double; 360 frames checked.');
}finally{await b.close()}
