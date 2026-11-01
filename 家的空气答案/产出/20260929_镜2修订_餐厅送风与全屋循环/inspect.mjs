import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const root=path.dirname(fileURLToPath(import.meta.url));
const require=createRequire(path.resolve(root,'../20260929_第四期_木质大宽厅双方案/制作文件/final-qa.mjs'));
const {chromium}=require('playwright');
const browser=await chromium.launch({executablePath:'/Users/weipeilong/.cache/hyperframes/chrome/chrome-headless-shell/mac_arm-152.0.7977.30/chrome-headless-shell-mac-arm64/chrome-headless-shell',headless:true,timeout:20000,args:['--allow-file-access-from-files']});
const page=await browser.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:.5});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const results=[];
for(const key of ['镜2_A','镜2_B']){
 await page.goto(pathToFileURL(path.join(root,'HyperFrames工程',key,'index.html')).href,{waitUntil:'domcontentloaded',timeout:15000});
 const samples=[];
 for(const t of [.5,1.4,2.4,4,5.6]){
  await page.evaluate(t=>{window.seek(t)},t);
  samples.push(await page.evaluate(()=>({supplyOffset:getComputedStyle(document.querySelector('.supply-moving')).strokeDashoffset,circulationOffset:getComputedStyle(document.querySelector('#circulation-moving')).strokeDashoffset,supplyOpacity:getComputedStyle(document.querySelector('#airflow')).opacity,circulationOpacity:getComputedStyle(document.querySelector('#circulation')).opacity})));
 }
 await page.evaluate(()=>{window.seek(4)});
 await page.screenshot({path:path.join(root,'预览图',key+'_工程预览.png')});
 const details=await page.evaluate(()=>{
  const vent=document.querySelector('#vent').getBBox();
  const paths=[...document.querySelectorAll('.supply-base')].map(p=>{const a=p.getPointAtLength(0),b=p.getPointAtLength(p.getTotalLength());return{start:{x:a.x,y:a.y},end:{x:b.x,y:b.y},rightToLeft:a.x>b.x}});
  const walker=document.createTreeWalker(document.querySelector('#main'),NodeFilter.SHOW_TEXT);let n,text='';while(n=walker.nextNode())text+=n.textContent.trim();
  const choreography=window.__timelines.main.getChildren(false,true,false).map(t=>({start:t.startTime(),duration:t.duration(),targets:t.targets().map(x=>x.id||x.getAttribute('class')),properties:Object.keys(t.vars).filter(k=>!['duration','ease','parent','immediateRender','runBackwards','overwrite','delay'].includes(k))}));
  return{vent:{x:vent.x,y:vent.y,width:vent.width,height:vent.height},paths,text,choreography};
 });
 if(details.text||details.paths.length!==14||details.paths.some(p=>!p.rightToLeft)||details.vent.x<500)throw new Error('Direction/location/text check failed '+key);
 if(samples[3].supplyOffset===samples[4].supplyOffset||samples[3].circulationOffset===samples[4].circulationOffset)throw new Error('Airflow does not move '+key);
 results.push({key,details,samples});
}
await browser.close();if(errors.length)throw new Error(errors.join('\n'));
await fs.writeFile(path.join(root,'制作文件/风向与时间轴检查.json'),JSON.stringify({errors,results},null,2));
console.log('Both dining-side outlets, 28 right-to-left supply paths, both moving circulation paths and no text: verified');
