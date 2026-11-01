/* v4 — readable filter, full ?, no Mini ghost during D wipe */
const W=1080,H=1920,FPS=30,DUR=20;
const COLORS={paper:'#F5F2ED',coffee:'#433538',gold:'#C4A574',olive:'#6B6B47',deep:'#3B2F2C'};
const canvas=document.getElementById('c');
const ctx=canvas.getContext('2d');
const tEl=document.getElementById('t');
const assets={};
const ASSET_LIST=[
  ['paper','../assets/gen/paper_texture.png'],
  ['window','../assets/gen/window_closed.png'],
  ['wall','../assets/gen/wall_cutaway.png'],
  ['duct','../assets/gen/duct_paper.png'],
  ['core','../assets/gen/core_plates.png'],
  ['warm','../assets/gen/airflow_strip_warm.png'],
  ['cool','../assets/gen/airflow_strip_cool.png'],
  ['filter','../assets/gen/filter_sheet_hi.png'],
  ['table','../assets/gen/table_surface.png'],
  ['mini','../assets/official/mini_cutout.png'],
  ['logo','../assets/official/logo_1-1.png'],
];
function loadImg(src){return new Promise(res=>{const i=new Image();i.onload=()=>res(i);i.onerror=()=>res(null);i.src=src;});}
async function loadAll(){await Promise.all(ASSET_LIST.map(async([k,p])=>{assets[k]=await loadImg(p);}));}
function easeInOut(t){return t<.5?2*t*t:-1+(4-2*t)*t;}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function lerp(a,b,t){return a+(b-a)*t;}
function drawPaper(ctx){
  if(assets.paper){ctx.drawImage(assets.paper,0,0,W,H);}
  else{ctx.fillStyle=COLORS.paper;ctx.fillRect(0,0,W,H);}
}
function drawHandLine(ctx,pts,progress,lw=3){
  if(progress<=0||pts.length<2)return;
  const n=Math.floor((pts.length-1)*clamp(progress,0,1));
  ctx.strokeStyle=COLORS.coffee;ctx.lineWidth=lw;ctx.lineCap='round';ctx.lineJoin='round';
  ctx.beginPath();ctx.moveTo(pts[0][0],pts[0][1]);
  for(let i=1;i<=n;i++)ctx.lineTo(pts[i][0],pts[i][1]);
  if(n<pts.length-1){const f=(pts.length-1)*clamp(progress,0,1)-n;const a=pts[n],b=pts[n+1];ctx.lineTo(lerp(a[0],b[0],f),lerp(a[1],b[1],f));}
  ctx.stroke();
}
function drawImg(ctx,img,x,y,w,h,rot=0,alpha=1){
  if(!img||alpha<=0)return;
  ctx.save();ctx.globalAlpha=alpha;ctx.translate(x+w/2,y+h/2);ctx.rotate(rot);
  ctx.drawImage(img,-w/2,-h/2,w,h);ctx.restore();
}
function drawQuestion(ctx,p){
  /* Readable handwritten "?" via system script fonts (not a loading ring) */
  if(p<=0)return;
  const cx=800, cy=420;
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(-0.08);
  const sc=lerp(0.7,1,easeInOut(Math.min(p*1.2,1)));
  ctx.scale(sc,sc);
  ctx.globalAlpha=clamp(p*1.4,0,1);
  ctx.fillStyle=COLORS.coffee;
  ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.font='700 220px "Marker Felt","Noteworthy","Bradley Hand","Segoe Print",cursive,sans-serif';
  ctx.fillText('?',0,0);
  // soft ink offset for craft feel
  ctx.globalAlpha=clamp(p*1.4,0,1)*0.22;
  ctx.fillText('?',3,4);
  ctx.restore();
}
function proceduralAirflow(ctx,t,warm){
  const path=[]; const x0=warm?160:920,y0=warm?700:1200;
  for(let i=0;i<=40;i++){
    const u=i/40;
    path.push([lerp(x0,warm?920:160,u)+Math.sin(u*Math.PI*2+t)*(warm?36:-36), lerp(y0,warm?1200:700,u)+Math.cos(u*Math.PI*1.5)*28]);
  }
  const prog=clamp(t,0,1); if(prog<=0)return;
  ctx.save();ctx.strokeStyle=warm?COLORS.gold:COLORS.olive;ctx.lineWidth=12;ctx.lineCap='round';ctx.globalAlpha=.75;
  ctx.beginPath();const n=Math.max(1,Math.floor(40*prog));ctx.moveTo(path[0][0],path[0][1]);
  for(let i=1;i<=n;i++)ctx.lineTo(path[i][0],path[i][1]);ctx.stroke();ctx.restore();
}
function drawDustParticles(ctx,progress){
  const flecks=[
    [340,1080,8],[410,1140,6],[480,1100,10],[560,1160,7],[620,1110,9],
    [380,1200,5],[520,1220,8],[450,1260,6],[590,1250,7],[500,1180,5],
    [360,1120,6],[640,1190,8],[430,1170,7],[550,1090,6],[470,1235,9],
    [700,1140,5],[300,1180,6],[650,1260,7],
  ];
  const n=Math.floor(flecks.length*clamp(progress,0,1));
  for(let i=0;i<n;i++){
    const [x,y,r]=flecks[i];
    ctx.fillStyle=COLORS.deep;ctx.globalAlpha=0.65;
    ctx.beginPath();ctx.ellipse(x,y+(1-progress)*50,r,r*0.7,0.15,0,Math.PI*2);ctx.fill();
  }
  ctx.globalAlpha=1;
}

function sceneA(t){
  const a=clamp(t/2.6,0,1);
  const ay=lerp(-480,400,easeInOut(a));
  const sc=lerp(1.06,1,easeInOut(a));
  const ww=760*sc,wh=980*sc,wx=(W-ww)/2;
  drawImg(ctx,assets.window,wx,ay,ww,wh,(1-a)*-0.05,clamp(a*1.3,0,1));
  if(t>0.85) drawQuestion(ctx,clamp((t-0.85)/1.5,0,1));
}
function sceneB(t){
  const b=t;
  const zoom=lerp(1,1.26,easeInOut(clamp((b-.15)/.7,0,1)));
  ctx.save();ctx.translate(W/2,H*.48);ctx.scale(zoom,zoom);ctx.translate(-W/2,-H*.48);
  const wf=1-clamp(b/.3,0,1);
  if(wf>0.02) drawImg(ctx,assets.window,160,400,760,900,0,wf*.3);
  drawImg(ctx,assets.wall,90,220,900,1200,0,clamp(b*1.6,0,1));
  if(b>0.25) drawImg(ctx,assets.duct,300,760,480,420,(1-clamp((b-.25)/.35,0,1))*.15,clamp((b-.25)/.35,0,1));
  ctx.restore();
}
function sceneC(t){
  const c=t;
  drawImg(ctx,assets.wall,140,260,800,1000,0,0.18*(1-c));
  const s=lerp(.78,1,easeInOut(c));
  drawImg(ctx,assets.core,W/2-420*s,H*.34,840*s,840*s,0,clamp(c*1.5,0,1));
  if(c>0.18){
    proceduralAirflow(ctx,(c-.18)/.55,true);
    proceduralAirflow(ctx,(c-.18)/.55,false);
    drawImg(ctx,assets.warm,40,620,420,900,-0.1,clamp((c-.18)/.4,0,.65));
    drawImg(ctx,assets.cool,620,620,420,900,0.1,clamp((c-.18)/.4,0,.65));
  }
}
function sceneD(t){
  const d=Math.max(t,0.001);
  // room card with gold edge — always visible
  ctx.save();
  ctx.globalAlpha=0.55;
  ctx.fillStyle='#E8E0D4';
  ctx.fillRect(90,360,900,860);
  ctx.restore();
  ctx.strokeStyle=COLORS.gold;ctx.lineWidth=3;ctx.globalAlpha=0.9;
  ctx.strokeRect(110,380,860,820);ctx.globalAlpha=1;

  // filter: scale+drop, always high opacity, multiply for paper contrast
  const fy=lerp(420,680,easeInOut(d));
  const fs=lerp(0.88,1.0,easeInOut(d));
  const fw=700*fs, fh=700*fs, fx=W/2-fw/2;
  ctx.save();
  ctx.globalAlpha=clamp(0.55+d*0.5,0,1);
  ctx.translate(fx+fw/2,fy+fh/2);
  ctx.rotate(-0.04*(1-d));
  if(assets.filter){
    ctx.drawImage(assets.filter,-fw/2,-fh/2,fw,fh);
  } else {
    // procedural filter card fallback
    ctx.fillStyle='#D9D0C4';ctx.fillRect(-fw/2,-fh/2,fw,fh);
    ctx.strokeStyle=COLORS.coffee;ctx.lineWidth=4;ctx.strokeRect(-fw/2+8,-fh/2+8,fw-16,fh-16);
  }
  // coffee mesh overlay for readability
  ctx.strokeStyle='rgba(67,53,56,0.35)';ctx.lineWidth=1.5;
  for(let i=-5;i<=5;i++){
    ctx.beginPath();ctx.moveTo(-fw*0.35,i*fh*0.06);ctx.lineTo(fw*0.35,i*fh*0.06);ctx.stroke();
  }
  ctx.restore();

  if(d>0.2) drawDustParticles(ctx,clamp((d-.2)/.55,0,1));
}
function sceneE(t){
  const e=t;
  if(assets.table) drawImg(ctx,assets.table,0,1180,W,740,0,e);
  else {ctx.fillStyle='#E8DFD2';ctx.globalAlpha=e;ctx.fillRect(0,1280,W,640);ctx.globalAlpha=1;}
  const my=lerp(540,900,easeInOut(e));
  const mScale=lerp(1.1,1,easeInOut(e));
  const mw=700*mScale, mh=500*mScale, mx=(W-mw)/2;
  ctx.save();ctx.globalAlpha=.28*e;
  ctx.fillStyle='#000';ctx.beginPath();ctx.ellipse(W/2,my+mh*.88,mw*.36,26,0,0,Math.PI*2);ctx.fill();
  ctx.restore();
  drawImg(ctx,assets.mini,mx,my,mw,mh,0,clamp(e*1.3,0,1));
  if(e>0.45 && assets.logo) drawImg(ctx,assets.logo,W/2-170,1680,340,130,0,clamp((e-.45)/.35,0,1));
}

function frame(t){
  drawPaper(ctx);
  if(t<3.8){
    sceneA(t);
    if(t>3.3){const k=clamp((t-3.3)/.5,0,1);ctx.fillStyle=`rgba(245,242,237,${.5*k})`;ctx.fillRect(0,0,W,H);sceneB(k*0.12);}
  } else if(t<7.6){
    sceneB(clamp((t-3.8)/3.8,0,1));
  } else if(t<11.8){
    const c0=clamp((t-7.6)/4.2,0,1);
    if(c0<0.12){sceneB(1);ctx.fillStyle=`rgba(245,242,237,${c0/0.12*.7})`;ctx.fillRect(0,0,W,H);}
    sceneC(c0);
  } else if(t<15.6){
    const d0=clamp((t-11.8)/3.8,0,1);
    if(d0<0.1){sceneC(1);ctx.fillStyle=`rgba(245,242,237,${d0/0.1*.75})`;ctx.fillRect(0,0,W,H);}
    sceneD(d0);
  } else {
    // Hard wipe then Mini — never overlap product with filter/dust
    const e0=clamp((t-15.6)/4.4,0,1);
    const wipe=clamp(e0/0.12,0,1);
    if(wipe<1){sceneD(1);ctx.fillStyle=`rgba(245,242,237,${wipe})`;ctx.fillRect(0,0,W,H);}
    else {drawPaper(ctx);sceneE(clamp((e0-0.12)/0.88,0,1));}
  }
}

let start=performance.now();
function loop(now){
  const forced=window.__FORCE_T;
  const tt=forced==null?(((now-start)/1000)%DUR):forced;
  tEl.textContent=tt.toFixed(2);
  ctx.clearRect(0,0,W,H);frame(tt);
  if(forced==null) requestAnimationFrame(loop);
}
loadAll().then(()=>requestAnimationFrame(loop));
window.__seek=(sec)=>{window.__FORCE_T=sec;frame(sec);};
window.__renderAt=(sec)=>{window.__FORCE_T=sec;ctx.clearRect(0,0,W,H);frame(sec);};
