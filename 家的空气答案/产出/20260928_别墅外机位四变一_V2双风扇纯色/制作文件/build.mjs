import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const dir=path.join(root,'HyperFrames工程');
function fan(cy){return `<g class="fan" transform="translate(38 ${cy})"><circle class="fan-rim" r="32" fill="#F5EFE3" stroke="#B69B61" stroke-width="2"/>${[15,21,27].map(r=>`<circle r="${r}" fill="none" stroke="#A49681" stroke-width=".6" opacity=".7"/>`).join('')}${Array.from({length:12},(_,i)=>`<path d="M0 -30C-15 -22 -14 -5 0 0" transform="rotate(${i*30})" fill="none" stroke="#A49681" stroke-width=".6" opacity=".7"/>`).join('')}<circle r="8.5" fill="#D9C7A0" stroke="#B69B61" stroke-width="1"/></g>`}
function unit(id,x,y){return `<g transform="translate(${x} ${y})"><g id="${id}" class="machine" data-part="${id}">
 <rect class="bay" x="-10" y="-10" width="124" height="181" rx="6" fill="#EDE3CE" fill-opacity=".45" stroke="#B69B61" stroke-width="1.2"/>
 <path d="M17 155V161H28V155M78 155V161H89V155" fill="#E2D7C6" stroke="#948678" stroke-width="1.5"/>
 <rect class="cabinet" x="0" y="0" width="104" height="155" rx="1.6" fill="#F3ECE2" stroke="#948678" stroke-width="2.2"/>
 <path d="M1 3H103M72 3V152M3 3V152H101M1 151H103" fill="none" stroke="#948678" stroke-width=".9"/>
 <path d="M7 -1H97" fill="none" stroke="#948678" stroke-width="1.5"/>
 ${fan(40)}${fan(115)}
 <path d="M8 148H15M57 148H64M82 148H92" stroke="#A49681" stroke-width="1"/>
 </g></g>`}
const svg=`<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg" aria-label="别墅室外四个外机位减少为一个的无文字示意动画">
<g id="backdrop"><rect width="1080" height="1920" fill="#E9DFD2"/></g>
<g id="illustration" stroke-linejoin="round" stroke-linecap="round">
 <g id="garden-back" fill="none" stroke="#B7AA94" stroke-width="1.7">
  <path d="M953 1330V1028M953 1198C904 1163 900 1122 932 1083C901 1033 940 999 953 978C971 1006 1007 1043 978 1086C1011 1122 999 1171 953 1198" fill="#EAE2D2"/>
  <path d="M952 1160L932 1124M953 1093L972 1066"/>
 </g>
 <g id="ground" stroke="#B3A590" stroke-width="1.8"><path d="M100 1375L757 1375L982 1276L322 1276Z" fill="#EAE2D4"/><path d="M100 1375V1388H757L982 1289V1276M757 1375V1388" fill="#F6F1E8"/><path d="M338 1388L292 1450H460L502 1388M305 1433H471" fill="#F7F2E9"/></g>
 <g id="villa" stroke="#948678" stroke-width="2.4">
  <path d="M760 608L925 535V1284L760 1360Z" fill="#EAE1D1"/>
  <path d="M140 608H760V1360H140Z" fill="#F7F2E8"/>
  <path d="M140 1005H760L925 932" fill="none" stroke="#BCAD97" stroke-width="2"/>
  <path d="M140 1020H760L925 947" fill="none" stroke="#DACFBF" stroke-width="5"/>
  <path d="M120 585H760L946 500H310Z" fill="#F2EADB"/>
  <path d="M120 585V610H760L946 527V500L760 585" fill="#E6DCCB"/>
  <path d="M760 585V610" fill="none"/>
  <path d="M147 630H740" fill="none" stroke="#D8CBB7" stroke-width="1.4"/>
  <g id="front-windows" fill="#EDE3CE" stroke="#A49681" stroke-width="2.2">
   <rect x="182" y="670" width="208" height="130" rx="2"/><rect x="508" y="670" width="208" height="130" rx="2"/>
   <rect x="182" y="1063" width="208" height="90" rx="2"/><rect x="508" y="1063" width="208" height="90" rx="2"/>
   <path d="M286 670V800M612 670V800M286 1063V1153M612 1063V1153" fill="none"/>
   <path d="M196 684H272V786H196ZM522 684H598V786H522ZM196 1077H272V1139H196ZM522 1077H598V1139H522Z" fill="#FAF5EA" opacity=".65" stroke="none"/>
  </g>
  <g id="entry"><rect x="419" y="1136" width="60" height="224" fill="#D9CCB7" stroke="#A79882"/><path d="M435 1148V1346M447 1148V1346M459 1148V1346" stroke="#C0AF94" stroke-width="1.2"/><path d="M468 1236V1271" stroke="#948678" stroke-width="3"/></g>
  <g id="side-windows" fill="#E3D6BE" stroke="#A79882" stroke-width="1.8"><path d="M797 672L891 630V843L797 885Z"/><path d="M797 1069L891 1027V1224L797 1266Z"/><path d="M844 651V864M844 1048V1245" fill="none"/><path d="M808 684L834 672V847L808 858ZM808 1081L834 1069V1228L808 1239Z" fill="#F0E6D2" stroke="none"/></g>
  <g id="cladding" stroke="#D9CDBA" stroke-width="1.2"><path d="M418 635V980M433 635V980M448 635V980M463 635V980M478 635V980"/></g>
 </g>
 <g id="machines">${unit('unit-a',234,826)}${unit('unit-b',560,826)}${unit('unit-c',234,1178)}${unit('unit-d',560,1178)}</g>
 <g id="retained-accent" transform="translate(560 1178)" fill="none" stroke="#B69B61" stroke-width="2.2"><rect id="final-outline" x="-10" y="-10" width="124" height="181" rx="6"/></g>
 <g id="garden-front" stroke="#AEA087" stroke-width="1.6" fill="none"><path d="M95 1332V1255M95 1295C51 1292 62 1250 84 1241C83 1209 108 1211 114 1241C144 1256 130 1289 95 1295" fill="#E9E1CF"/><path d="M70 1332H122L116 1377H77Z" fill="#F0E8D9"/><path d="M88 1260L95 1283L111 1259"/><path d="M793 1400C808 1374 829 1370 846 1387C861 1357 886 1365 891 1384C916 1363 938 1381 941 1400Z" fill="#E7DFCE"/></g>
</g></svg>`;
const html=`<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><title>别墅外机位四变一</title><script src="gsap.min.js"></script><style>*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:transparent}#main{width:1080px;height:1920px;position:relative;background:transparent}.scene-content{width:100%;height:100%;padding:0;display:flex;flex-direction:column;gap:0}svg{width:100%;height:100%;flex:1}.machine{transform-box:fill-box;transform-origin:center}#retained-accent{opacity:0}.transparent #backdrop{display:none}</style></head><body><div id="main" class="clip" data-composition-id="main" data-start="0" data-duration="6" data-width="1080" data-height="1920" data-fps="60" data-track-index="0"><div class="scene-content">${svg}</div></div><script>
const tl=gsap.timeline({paused:true});
tl.from('#villa',{opacity:0,y:12,duration:.7,ease:'power3.out'},.15);
tl.from('#ground',{opacity:0,duration:.8,ease:'sine.out'},.16);
tl.from('#garden-back,#garden-front',{opacity:0,scale:.98,transformOrigin:'center bottom',duration:.65,ease:'power2.out'},.28);
tl.from('.machine',{opacity:0,scale:.95,y:8,duration:.5,stagger:.1,ease:'expo.out'},.42);
['#unit-a','#unit-b','#unit-c'].forEach((id,i)=>{tl.to(id,{opacity:0,scale:.88,y:-20,duration:.48,ease:'power2.in'},2+i*.32)});
tl.to('#retained-accent',{opacity:1,duration:.55,ease:'sine.out'},3.25);
const outline=document.querySelector('#final-outline');const len=outline.getTotalLength();gsap.set(outline,{strokeDasharray:len,strokeDashoffset:len});tl.to(outline,{strokeDashoffset:0,duration:.9,ease:'sine.inOut'},3.25);
tl.to('#unit-d .bay',{fillOpacity:.16,duration:.85,ease:'sine.inOut'},3.3);
tl.to('#retained-accent',{opacity:.48,duration:.7,ease:'power1.inOut'},4.25);
window.__timelines={main:tl};window.seek=t=>{tl.seek(t,false)};window.setTransparent=v=>document.body.classList.toggle('transparent',v!==false);if(new URLSearchParams(location.search).has('transparent'))window.setTransparent();
</script></body></html>`;
await fs.writeFile(path.join(dir,'index.html'),html);
const alphaDir=path.join(root,'透明工程');await fs.mkdir(alphaDir,{recursive:true});
await fs.writeFile(path.join(alphaDir,'index.html'),html.replace('<body>','<body class="transparent">'));
await fs.copyFile(path.join(dir,'gsap.min.js'),path.join(alphaDir,'gsap.min.js'));
await fs.copyFile(path.join(dir,'DESIGN.md'),path.join(alphaDir,'DESIGN.md'));
await fs.writeFile(path.join(dir,'package.json'),JSON.stringify({private:true,scripts:{check:'hyperframes check . --at-transitions',render:'hyperframes render . --fps 60 --quality high --workers 1 --output ../别墅外机位_四变一_无文字.mp4'}},null,2));
await fs.writeFile(path.join(alphaDir,'package.json'),JSON.stringify({private:true,scripts:{check:'hyperframes check . --at-transitions',render:'hyperframes render . --format mov --fps 60 --quality high --workers 1 --output ../别墅外机位_四变一_透明.mov'}},null,2));
await fs.writeFile(path.join(root,'制作文件/建筑线稿.svg'),svg);
console.log('Built villa composition');
