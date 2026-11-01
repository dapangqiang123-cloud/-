import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url)),dir=path.join(root,'HyperFrames工程');await fs.mkdir(dir,{recursive:true});await fs.mkdir(path.join(root,'制作文件'),{recursive:true});
await fs.copyFile('/Users/weipeilong/.codex/generated_images/01a0a5c8-b904-7e91-bfc1-ec819f67dbed/exec-fd04e0d3-cc36-46ec-a61d-e12badce2351.png',path.join(dir,'clean-plate.png'));
await fs.copyFile('/Users/weipeilong/Pictures/常用视觉库.library/images/MUL9NUMOMZJDU.info/exec-f80a5b42-ca36-43dd-9777-73de139ea021.png',path.join(root,'制作文件/用户原图.png'));
await fs.copyFile(path.resolve(root,'../20260929_第四期_浅咖无文字试样/HyperFrames工程/gsap.min.js'),path.join(dir,'gsap.min.js'));await fs.copyFile(path.join(root,'DESIGN.md'),path.join(dir,'DESIGN.md'));
const masks=[
 `<path d="M40 544V506H57V446H94V311L40 287V255H94V208L213 203V175H857L931 120H963V184H989V539H998V545Z"/><circle cx="123" cy="133" r="67"/><path d="M38 261V126H55V260ZM178 123H208V141H178ZM112 189H137V214H112Z"/>`,
 `<path d="M40 1053V1016H57V954H94V816L40 795V766H94V717L213 713V686H857L931 631H963V695H989V1048H998V1055Z"/><circle cx="122" cy="647" r="67"/><path d="M38 773V639H55V773ZM178 637H208V655H178ZM112 703H137V723H112Z"/>`,
 `<path d="M40 1480V1453H56V1398H94V1290L40 1268V1235H94V1205H197V1167H853L931 1119H963V1177H989V1475H998V1481Z"/><circle cx="122" cy="1147" r="67"/><path d="M38 1240V1139H55V1240ZM178 1139H209V1158H178ZM112 1203H137V1220H112Z"/>`
];
function winds(paths,kind){return paths.map((d,i)=>`<path class="base ${kind}-base" d="${d}" fill="none" stroke="#FFFFFF" stroke-width="2" opacity=".55"/><path class="moving ${kind}-moving" d="${d}" fill="none" stroke="#FFFFFF" stroke-width="${kind==='far'?2.8:4}" stroke-dasharray="26 67" stroke-dashoffset="${kind==='far'?i*6:0}" opacity="${kind==='far'?.78:.9}"/>`).join('');}
const downward=Array.from({length:24},(_,i)=>{const x=272+i*21;return `M${x} 232Q${x} 294 ${x+(i-11.5)*2.5} 410`});
const loop='M285 773H786C866 773 916 828 916 891C916 959 820 977 680 977H350C230 977 185 930 185 866C185 805 220 773 285 773Z';
const distant=Array.from({length:10},(_,i)=>`M232 ${1209+i*.8}C397 ${1260+i*5} 683 ${1250+i*8} 933 ${1268+i*7}`);
const panels=[
 `<g class="wind" id="wind1"><path d="M267 232H782L829 410H230Z" fill="url(#curtain)"/>${winds(downward,'down')}<g id="arrows1">${[307,449,596,738].map(x=>`<path class="drop-arrow" d="M${x} 271v37m-8-9l8 10l8-10" stroke="#FFFFFF" stroke-width="3" fill="none"/>`).join('')}</g></g>`,
 `<g class="wind" id="wind2"><path d="${loop}" fill="none" stroke="#FFFFFF" stroke-width="24" opacity=".15"/><path class="base loop-base" d="${loop}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity=".6"/><path class="moving loop-moving" d="${loop}" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-dasharray="57 110" opacity=".94"/></g>`,
 `<g id="outlet3" stroke="#8D7765" stroke-width="1.5"><path d="M224 1203l24 9m-24-5l24 9m-24-5l24 9"/></g><g class="wind" id="wind3">${winds(distant,'far')}</g>`
];
const html=`<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>三层科普风效动画</title><script src="gsap.min.js"></script><style>*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#F4EDE4}#main{width:1080px;height:1920px;background:#F4EDE4}.scene-content{width:100%;height:100%;padding:0 32px;display:flex;flex-direction:column;justify-content:center;gap:0}.figure{width:1016px;height:1500px;flex:none}svg{width:100%;height:100%;display:block;overflow:visible}</style></head><body><div id="main" class="clip" data-composition-id="main" data-start="0" data-duration="7" data-width="1080" data-height="1920" data-track-index="0"><div class="scene-content"><div class="figure"><svg viewBox="0 0 1032 1524" xmlns="http://www.w3.org/2000/svg" stroke-linecap="round" stroke-linejoin="round"><defs><linearGradient id="curtain" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#FFFFFF" stop-opacity=".22"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>${masks.map((m,i)=>`<clipPath id="cut${i+1}">${m}</clipPath>`).join('')}</defs>${panels.map((p,i)=>`<g class="panel" id="panel${i+1}"><image href="clean-plate.png" width="1032" height="1524" clip-path="url(#cut${i+1})"/>${p}</g>`).join('')}</svg></div></div></div><script>
const tl=gsap.timeline({paused:true});
[.2,1.7,3.2].forEach((start,i)=>{
 tl.from('#panel'+(i+1),{opacity:0,y:22,duration:.75,ease:['power3.out','sine.out','expo.out'][i]},start);
 tl.from('#wind'+(i+1),{opacity:0,duration:.55,ease:'sine.out'},start+.55);
 document.querySelectorAll('#wind'+(i+1)+' .base').forEach((p,j)=>{const n=p.getTotalLength();p.style.strokeDasharray=n;tl.from(p,{strokeDashoffset:n,duration:i===1?1.35:.9,ease:'sine.inOut'},start+.6+j*.008)});
 tl.from('#wind'+(i+1)+' .moving',{opacity:0,duration:.5,ease:'sine.out'},start+1);
 tl.to('#wind'+(i+1)+' .moving',{strokeDashoffset:(j,e)=>Number(e.getAttribute('stroke-dashoffset')||0)-(i===1?1550:850),duration:7-(start+1),ease:'none'},start+1);
});
tl.from('#arrows1',{opacity:0,duration:.5,ease:'power2.out'},1);
tl.fromTo('.drop-arrow',{y:0},{y:95,duration:1.4,repeat:3,ease:'none'},1.1);
window.__timelines={main:tl};window.seek=t=>{tl.seek(t,false)};
</script></body></html>`;
await fs.writeFile(path.join(dir,'index.html'),html);console.log(dir);
