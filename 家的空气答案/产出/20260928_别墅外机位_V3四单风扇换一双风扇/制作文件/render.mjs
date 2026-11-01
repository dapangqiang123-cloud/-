import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';import {spawn} from 'node:child_process';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),dir=path.join(root,'HyperFrames工程');
async function run(args,name){const out=[];const code=await new Promise((resolve,reject)=>{const p=spawn('/usr/local/bin/hyperframes',args,{cwd:dir});p.stdout.on('data',x=>out.push(x));p.stderr.on('data',x=>out.push(x));p.on('error',reject);p.on('close',resolve)});await fs.writeFile(path.join(root,'制作文件',name+'.log'),Buffer.concat(out));if(code)throw Error(name+' failed '+code);console.log(name+' OK')}
await run(['check','.','--json','--at-transitions'],'检查');
await run(['render','.','--fps','60','--quality','high','--workers','1','--output',path.join(root,'别墅外机位_四变一_无文字.mp4')],'1080P渲染');
await run(['render','.','--fps','60','--quality','high','--workers','1','--resolution','portrait-4k','--output',path.join(root,'别墅外机位_四变一_无文字_4K.mp4')],'4K渲染');
await run(['check',path.join(root,'透明工程'),'--json','--at-transitions'],'透明检查');
await run(['render',path.join(root,'透明工程'),'--fps','60','--format','mov','--quality','high','--workers','1','--output',path.join(root,'别墅外机位_四变一_透明.mov')],'透明渲染');
