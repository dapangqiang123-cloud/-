import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
const root=path.dirname(fileURLToPath(import.meta.url));
const scenes=JSON.parse(await fs.readFile(path.join(root,'制作文件/scenes.json'),'utf8'));
const out=[];
for(const s of scenes){
 const p=spawnSync('/opt/homebrew/bin/ffprobe',['-v','error','-show_streams','-show_format','-of','json',s.v4],{encoding:'utf8'});if(p.status)throw new Error(p.stderr);
 const m=JSON.parse(p.stdout),v=m.streams[0];
 if(v.width!==2160||v.height!==3840||v.r_frame_rate!=='60/1'||Number(m.format.duration)!==6||m.streams.length!==1)throw new Error('Incorrect format '+s.key);
 const hashes=[];
 for(const t of ['4','4.3']){const f=path.join(root,'预览图',s.key+'_t'+t+'.png');const r=spawnSync('/opt/homebrew/bin/ffmpeg',['-y','-v','error','-ss',t,'-i',s.v4,'-frames:v','1','-vf','scale=540:960',f]);if(r.status)throw new Error('frame extraction failed');hashes.push(createHash('sha256').update(await fs.readFile(f)).digest('hex'));}
 if(hashes[0]===hashes[1])throw new Error('Airflow stopped during hold');
 const log=await fs.readFile(path.join(root,'制作文件/检查日志',s.key+'_check.log'),'utf8');const check=JSON.parse(log.slice(log.indexOf('{')));if(!check.ok)throw new Error('check failed');
 await fs.access(s.v1);
 out.push({key:s.key,width:v.width,height:v.height,fps:v.r_frame_rate,duration:6,checkOK:check.ok,distinctMovingFrames:true});
}
await fs.writeFile(path.join(root,'制作文件/成片核验.json'),JSON.stringify(out,null,2));console.log(JSON.stringify(out,null,2));
