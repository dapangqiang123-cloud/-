import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawn} from 'node:child_process';
const root=path.dirname(fileURLToPath(import.meta.url));
const scenes=JSON.parse(await fs.readFile(path.join(root,'制作文件/scenes.json'),'utf8'));
async function run(bin,args,key){const chunks=[];const status=await new Promise((resolve,reject)=>{const p=spawn(bin,args);p.stdout.on('data',x=>chunks.push(x));p.stderr.on('data',x=>chunks.push(x));p.on('error',reject);p.on('close',resolve)});const log=Buffer.concat(chunks).toString();await fs.writeFile(path.join(root,'制作文件/检查日志',key+'.log'),log);if(status)throw new Error(key+' failed: '+log.slice(-1500));return log;}
let next=0;
async function worker(){while(next<scenes.length){const s=scenes[next++];
 await run('/usr/local/bin/hyperframes',['check',s.dir,'--json','--at-transitions'],s.key+'_check');
 console.log(s.key+' checks passed');
 if(!s.reused){await run('/usr/local/bin/hyperframes',['render',s.dir,'--resolution','portrait-4k','--fps','60','--workers','1','--quality','high','--output',s.v4],s.key+'_render');
 await run('/opt/homebrew/bin/ffmpeg',['-y','-v','error','-i',s.v4,'-vf','scale=1080:1920','-c:v','libx264','-crf','18','-preset','fast','-an','-movflags','+faststart',s.v1],s.key+'_preview');}
 await run('/opt/homebrew/bin/ffmpeg',['-y','-v','error','-ss','4','-i',s.v4,'-frames:v','1','-vf','scale=540:960',path.join(root,'预览图',s.key+'.png')],s.key+'_hero');
 await run('/opt/homebrew/bin/ffmpeg',['-y','-v','error','-i',s.v4,'-vf','fps=1,scale=180:320,tile=6x1','-frames:v','1',path.join(root,'预览图',s.key+'_时间序列.png')],s.key+'_sequence');
 console.log(s.key+' DONE '+(s.reused?'approved sample reused':'new render'));
}}
await Promise.all([worker(),worker()]);
console.log('BOTH REVISED SHOT 2 COMPLETE');
