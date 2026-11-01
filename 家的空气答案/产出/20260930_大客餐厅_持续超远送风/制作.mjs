import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath,pathToFileURL} from 'node:url';import {createRequire} from 'node:module';import {spawn} from 'node:child_process';
const root=path.dirname(fileURLToPath(import.meta.url)),dir=path.join(root,'HyperFrames工程');
await fs.mkdir(path.join(root,'制作文件'),{recursive:true});
const require=createRequire(path.resolve(root,'../20260929_第四期_木质大宽厅双方案/制作文件/final-qa.mjs')),{chromium}=require('playwright');
const browser=await chromium.launch({executablePath:'/Users/weipeilong/.cache/hyperframes/chrome/chrome-headless-shell/mac_arm-152.0.7977.30/chrome-headless-shell-mac-arm64/chrome-headless-shell',headless:true,timeout:20000,args:['--allow-file-access-from-files']});
const page=await browser.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:.5});await page.goto(pathToFileURL(path.join(dir,'index.html')).href,{waitUntil:'domcontentloaded',timeout:15000});
const samples=[];for(const t of [.2,1,2,3.4,5,6.8]){await page.evaluate(t=>{window.seek(t)},t);samples.push(await page.evaluate(()=>({streak:document.querySelector('.streak').style.strokeDashoffset,arrows:[...document.querySelectorAll('.arrow')].filter(e=>Number(getComputedStyle(e).opacity)>.1).length,bodyText:document.body.innerText})));await page.screenshot({path:path.join(root,'制作文件','预览_'+t+'.png')});}
const tweens=await page.evaluate(()=>window.__timelines.main.getChildren(true,true,false).map(t=>({start:t.startTime(),duration:t.duration(),targets:t.targets().map(e=>e.id)})));
await fs.writeFile(path.join(root,'制作文件/时间轴检查.json'),JSON.stringify({samples,tweens},null,2));await browser.close();console.log('PREVIEW READY');
if(process.argv.includes('--preview-only'))process.exit(0);
async function run(bin,args,name){const chunks=[];const code=await new Promise((resolve,reject)=>{const p=spawn(bin,args);p.stdout.on('data',x=>chunks.push(x));p.stderr.on('data',x=>chunks.push(x));p.on('error',reject);p.on('close',resolve)});const log=Buffer.concat(chunks).toString();await fs.writeFile(path.join(root,'制作文件',name+'.log'),log);if(code)throw new Error(log.slice(-2500));console.log(name+' OK');}
await run('/usr/local/bin/hyperframes',['check',dir,'--json','--at-transitions'],'check');
const mp4=path.join(root,'大客餐厅_持续超远送风_7秒_4K.mp4');
await run('/usr/local/bin/hyperframes',['render',dir,'--resolution','portrait-4k','--fps','60','--workers','1','--quality','high','--output',mp4],'render');
await run('/opt/homebrew/bin/ffmpeg',['-y','-v','error','-i',mp4,'-vf','scale=1080:1920','-c:v','libx264','-crf','18','-preset','fast','-an','-movflags','+faststart',path.join(root,'大客餐厅_持续超远送风_7秒_1080预览.mp4')],'preview');
await run('/opt/homebrew/bin/ffmpeg',['-y','-v','error','-ss','4','-i',mp4,'-frames:v','1','-vf','scale=540:960',path.join(root,'成片预览.png')],'hero');
await run('/opt/homebrew/bin/ffmpeg',['-y','-v','error','-i',mp4,'-vf','fps=1,scale=180:320,tile=7x1','-frames:v','1',path.join(root,'制作文件/成片时间序列.png')],'sequence');
await run('/opt/homebrew/bin/ffprobe',['-v','error','-show_streams','-show_format','-of','json',mp4],'ffprobe');console.log('COMPLETE');

