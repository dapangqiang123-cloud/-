import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const source=path.resolve(root,'../20260929_第四期_木质大宽厅双方案/动画工程/镜5_A');
const dir=path.join(root,'HyperFrames工程');
await fs.mkdir(dir,{recursive:true});
let old=await fs.readFile(path.join(source,'index.html'),'utf8');
let svg=old.match(/<svg[\s\S]*?<\/svg>/)[0];
const colors={'#E0E5D7':'#E4D6C7','#E8EADD':'#EEE4D8','#D1D8C5':'#DAC8B7','#697453':'#A58D78','#A7AA99':'#C2AC97','#F3F3EA':'#F7F1E9','#414439':'#8D7765'};
svg=svg.replace(/#[A-Fa-f0-9]{6}/g,c=>colors[c]||c).replace('viewBox="0 0 920 690"','viewBox="25 -20 885 655"');
const html=`<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>璀璨浅咖无文字空气循环试样</title><script src="gsap.min.js"></script><style>
*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#F4EDE4}#main{position:relative;width:1080px;height:1920px;background:#F4EDE4;overflow:hidden}.scene-content{width:100%;height:100%;padding:64px 40px;display:flex;flex-direction:column;justify-content:center;gap:0}.figure{width:1000px;height:740px;flex:none}.figure svg{display:block;width:100%;height:100%;overflow:visible}
</style></head><body><div id="main" class="clip" data-composition-id="main" data-start="0" data-duration="7" data-width="1080" data-height="1920" data-track-index="0"><div class="scene-content"><div class="figure" id="figure">${svg}</div></div></div><script>
const tl=gsap.timeline({paused:true});
tl.from('#architecture',{opacity:0,y:12,duration:.8,ease:'power3.out'},.15);
document.querySelectorAll('.trace,.airline').forEach((p,i)=>{const n=p.getTotalLength();p.style.strokeDasharray=n;p.style.strokeDashoffset=0;tl.from(p,{strokeDashoffset:n,duration:1.3,ease:'sine.inOut'},.7+(i%12)*.018)});
tl.from('#airflow',{opacity:0,duration:.65,ease:'expo.out'},.6);
tl.from('.moving',{opacity:0,duration:.55,ease:'sine.out'},1.3);
tl.to('.moving',{strokeDashoffset:-560,duration:5,ease:'none'},1.5);
window.__timelines={main:tl};window.seek=t=>tl.seek(t,false);
</script></body></html>`;
await fs.writeFile(path.join(dir,'index.html'),html);
await fs.copyFile(path.join(source,'gsap.min.js'),path.join(dir,'gsap.min.js'));
await fs.copyFile(path.join(root,'DESIGN.md'),path.join(dir,'DESIGN.md'));
await fs.writeFile(path.join(dir,'package.json'),JSON.stringify({private:true,scripts:{check:'hyperframes check . --json --at-transitions'}}));
console.log(dir);
