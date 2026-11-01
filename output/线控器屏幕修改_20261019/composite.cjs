const fs = require('fs');
const path = require('path');
const sharp = require('/Users/weipeilong/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');

const root = __dirname;
const inputRoot = '/var/folders/nz/ln59_g0j4jz7dpl9yp1xqz5c0000gn/T';
const targets = [
  {
    input: 'codex-clipboard-9a99d59d-0c14-430f-b182-187cfc6a20fa.png',
    name: '图1_正视_除湿68.0.png',
    quad: [[109,113],[876,113],[876,617],[109,617]],
    noise: 0,
  },
  {
    input: 'codex-clipboard-e1065d6a-78cb-4bae-b90d-9ef08e90f7b3.png',
    name: '图2_透视_除湿68.0.png',
    quad: [[969,595],[1622,526],[1609,974],[983,1086]],
    noise: 2.5,
  },
];

function solve(A,b) {
  const n=b.length, m=A.map((r,i)=>[...r,b[i]]);
  for(let i=0;i<n;i++) {
    let p=i;
    for(let j=i+1;j<n;j++) if(Math.abs(m[j][i])>Math.abs(m[p][i])) p=j;
    [m[i],m[p]]=[m[p],m[i]];
    const d=m[i][i];
    if(Math.abs(d)<1e-12) throw new Error('Singular system');
    for(let j=i;j<=n;j++) m[i][j]/=d;
    for(let k=0;k<n;k++) if(k!==i) {
      const f=m[k][i];
      for(let j=i;j<=n;j++) m[k][j]-=f*m[i][j];
    }
  }
  return m.map(r=>r[n]);
}

function homography(src,dst) {
  const A=[],b=[];
  for(let i=0;i<4;i++) {
    const [x,y]=src[i],[u,v]=dst[i];
    A.push([x,y,1,0,0,0,-u*x,-u*y]); b.push(u);
    A.push([0,0,0,x,y,1,-v*x,-v*y]); b.push(v);
  }
  return [...solve(A,b),1];
}
function project(h,x,y) {
  const d=h[6]*x+h[7]*y+h[8];
  return [(h[0]*x+h[1]*y+h[2])/d,(h[3]*x+h[4]*y+h[5])/d];
}
function basis(u,v) {return [1,u,v,u*u,u*v,v*v];}
function dot(a,b) {return a.reduce((s,v,i)=>s+v*b[i],0);}
function fit(samples) {
  const A=Array.from({length:6},()=>Array(6).fill(0));
  const B=Array.from({length:3},()=>Array(6).fill(0));
  for(const s of samples) for(let i=0;i<6;i++) {
    for(let j=0;j<6;j++) A[i][j]+=s.f[i]*s.f[j];
    for(let c=0;c<3;c++) B[c][i]+=s.f[i]*s.rgb[c];
  }
  return B.map(b=>solve(A,b));
}
function luma(r,g,b) {return .2126*r+.7152*g+.0722*b;}
function clamp(x,a,b) {return Math.min(b,Math.max(a,x));}

(async()=>{
  const ui = await sharp(path.join(root,'UI图形底稿.png')).removeAlpha().raw().toBuffer({resolveWithObject:true});
  const {width:uw,height:uh,channels:uc}=ui.info;
  const alpha = new Float32Array(uw*uh);
  for(let i=0;i<alpha.length;i++) {
    const lum=luma(ui.data[i*uc],ui.data[i*uc+1],ui.data[i*uc+2]);
    alpha[i]=lum>=245?0:clamp((245-lum)/235,0,1);
  }
  function texture(u,v) {
    const x=clamp(u*(uw-1),0,uw-1),y=clamp(v*(uh-1),0,uh-1);
    const x0=Math.floor(x), y0=Math.floor(y), x1=Math.min(x0+1,uw-1),y1=Math.min(y0+1,uh-1);
    const fx=x-x0,fy=y-y0;
    return alpha[y0*uw+x0]*(1-fx)*(1-fy)+alpha[y0*uw+x1]*fx*(1-fy)+alpha[y1*uw+x0]*(1-fx)*fy+alpha[y1*uw+x1]*fx*fy;
  }
  const report=[];
  for(const t of targets) {
    const original=await sharp(path.join(inputRoot,t.input)).ensureAlpha().raw().toBuffer({resolveWithObject:true});
    const {width:w,height:h}=original.info;
    const data=original.data, result=Buffer.from(data);
    const inv=homography(t.quad,[[0,0],[1,0],[1,1],[0,1]]);
    const minX=Math.floor(Math.min(...t.quad.map(p=>p[0]))),maxX=Math.ceil(Math.max(...t.quad.map(p=>p[0])));
    const minY=Math.floor(Math.min(...t.quad.map(p=>p[1]))),maxY=Math.ceil(Math.max(...t.quad.map(p=>p[1])));
    const cells=[]; const samples=[];
    for(let y=minY;y<=maxY;y++) for(let x=minX;x<=maxX;x++) {
      const [u,v]=project(inv,x+.5,y+.5);
      if(u<0||u>1||v<0||v>1) continue;
      const i=(y*w+x)*4,f=basis(u,v),rgb=[data[i],data[i+1],data[i+2]];
      cells.push({x,y,u,v,i,f,rgb});
      const l=luma(...rgb);
      if(x%3===0&&y%3===0&&u>.02&&u<.98&&v>.02&&v<.98&&l>65&&l<190) samples.push({f,rgb});
    }
    let model=fit(samples);
    for(let n=0;n<4;n++) {
      const good=samples.filter(s=>{
        const e=luma(...s.rgb)-luma(...model.map(c=>dot(c,s.f)));
        return e>-3.8&&e<4.5;
      });
      model=fit(good);
    }
    const glyphMask=new Uint8Array(w*h);
    const threshold=t.noise?7:1.5;
    let darkCount=0;
    for(const s of cells) {
      const expected=model.map(c=>dot(c,s.f));
      if(luma(...expected)-luma(...s.rgb)>threshold) {
        glyphMask[s.y*w+s.x]=1; darkCount++;
      }
    }
    const repairMask=new Uint8Array(w*h);
    for(const s of cells) if(glyphMask[s.y*w+s.x]) {
      for(let dy=-2;dy<=2;dy++) for(let dx=-2;dx<=2;dx++) repairMask[(s.y+dy)*w+s.x+dx]=1;
    }
    // Preserve every clean source LCD pixel. Reconstruct only old ink and its antialiasing fringe.
    for(const s of cells) {
      let bg=s.rgb;
      const predicted=model.map(c=>dot(c,s.f));
      if(repairMask[s.y*w+s.x]) {
        bg=predicted;
        if(t.noise) {
          const offsets=[[29,17],[-31,23],[17,-29],[-19,-37],[47,31],[-43,-23],[61,-11],[-59,13]];
          for(const [dx,dy] of offsets) {
            const xx=s.x+dx,yy=s.y+dy;
            if(xx<minX||xx>maxX||yy<minY||yy>maxY||repairMask[yy*w+xx]) continue;
            const [u,v]=project(inv,xx+.5,yy+.5);
            if(u<.01||u>.99||v<.01||v>.99) continue;
            const f=basis(u,v),i=(yy*w+xx)*4;
            bg=predicted.map((p,c)=>p+clamp(data[i+c]-dot(model[c],f),-4,4));
            break;
          }
        }
      }
      let a=0;
      // Supersampled projection keeps thin LCD strokes clean at both output sizes.
      for(const dy of [.25,.75]) for(const dx of [.25,.75]) {
        const [u,v]=project(inv,s.x+dx,s.y+dy);
        a+=texture(u,v)*.25;
      }
      const ink=[6,7,5];
      for(let c=0;c<3;c++) result[s.i+c]=clamp(Math.round(bg[c]*(1-a)+ink[c]*a),0,255);
    }
    const out=path.join(root,t.name);
    await sharp(result,{raw:{width:w,height:h,channels:4}}).png({compressionLevel:9}).toFile(out);
    const saved=await sharp(out).ensureAlpha().raw().toBuffer();
    let changed=0,outside=0,maxOutside=0,alphaChanges=0;
    for(let y=0;y<h;y++) for(let x=0;x<w;x++) {
      const i=(y*w+x)*4;
      let d=0;for(let c=0;c<4;c++) d=Math.max(d,Math.abs(saved[i+c]-data[i+c]));
      if(saved[i+3]!==data[i+3]) alphaChanges++;
      if(d) {
        changed++;
        const [u,v]=project(inv,x+.5,y+.5);
        if(u<0||u>1||v<0||v>1) {outside++;maxOutside=Math.max(maxOutside,d);}
      }
    }
    if(outside||alphaChanges) throw new Error('Original pixel preservation check failed');
    report.push({file:t.name,width:w,height:h,editableScreenQuad:t.quad,changedPixels:changed,changedPixelsOutsideScreen:outside,maxOutsideChannelDifference:maxOutside,alphaChanges,oldInkPixels:darkCount,backgroundModel:model});
    await sharp(out).resize({width:Math.min(w,1400)}).png().toFile(path.join(root,t.name.replace('.png','_预览.png')));
    console.log(JSON.stringify(report.at(-1)));
  }
  fs.writeFileSync(path.join(root,'像素核验.json'),JSON.stringify(report,null,2));
})();
