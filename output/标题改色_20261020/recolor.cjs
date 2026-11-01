const fs = require('fs');
const path = require('path');
const sharp = require('/Users/weipeilong/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const sourceRoot = '/Users/weipeilong/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/weipeilong001_1cb6/temp/RWTemp/2026-10/2d016e8754281a8ba45277dcf6a806b1';
const reference = '/var/folders/nz/ln59_g0j4jz7dpl9yp1xqz5c0000gn/T/codex-clipboard-3a406649-db6d-4e87-a0f2-aa6ada6aedd8.png';
const files = [
  ['d5ce3f51ff7e39f975ae115101afde2e.png','01_秋渐深_雨添凉_复古橄榄绿.png'],
  ['19f4e6e8f7cdf9488a086a7a51c0cbaa.png','02_智慧除湿_精准控温_复古橄榄绿.png'],
  ['7d145169e2807abbb17a034266b37221.png','03_璀璨中央空调C3D系列_复古橄榄绿.png'],
];
const oldColor = [76,47,24];
const shadowColor = [112,81,56];
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));

(async()=>{
  const ref=await sharp(reference).removeAlpha().raw().toBuffer({resolveWithObject:true});
  const hist=new Map();
  for(let i=0;i<ref.data.length;i+=3){
    const rgb=[ref.data[i],ref.data[i+1],ref.data[i+2]];
    if(Math.max(...rgb)>155||Math.min(...rgb)>120||rgb[0]-rgb[2]<15)continue;
    const key=rgb.join(',');hist.set(key,(hist.get(key)||0)+1);
  }
  const [sample,sampleCount]=[...hist].sort((a,b)=>b[1]-a[1])[0];
  const newColor=sample.split(',').map(Number);
  const direction=shadowColor.map((c,k)=>c-oldColor[k]);
  const length2=direction.reduce((s,n)=>s+n*n,0);
  const reports=[];
  const previews=[];
  for(const [input,name] of files){
    const source=await sharp(path.join(sourceRoot,input)).ensureAlpha().raw().toBuffer({resolveWithObject:true});
    const {width:w,height:h}=source.info,data=source.data,out=Buffer.from(data);
    let mask=new Uint8Array(w*h);
    let coreCount=0;
    for(let p=0;p<w*h;p++){
      const i=p*4;
      if(data[i+3]&&oldColor.every((c,k)=>data[i+k]===c)) {mask[p]=1;coreCount++;}
    }
    // Dilate only the original glyph core to include its 1–2 px antialiased edge.
    for(let n=0;n<3;n++){
      const next=new Uint8Array(mask);
      for(let y=1;y<h-1;y++)for(let x=1;x<w-1;x++)if(mask[y*w+x]){
        for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++)next[(y+dy)*w+x+dx]=1;
      }
      mask=next;
    }
    let changed=0,edgeCount=0,unchangedWhite=0,unchangedShadow=0;
    const recoloredMask=new Uint8Array(w*h);
    for(let p=0;p<w*h;p++){
      const i=p*4;
      if(!mask[p]||!data[i+3])continue;
      const rgb=[data[i],data[i+1],data[i+2]];
      let weight=0;
      if(oldColor.every((c,k)=>rgb[k]===c))weight=1;
      else {
        const rawWeight=direction.reduce((s,d,k)=>s+(shadowColor[k]-rgb[k])*d,0)/length2;
        const residual=Math.sqrt(rgb.reduce((s,c,k)=>s+(c-(shadowColor[k]-rawWeight*direction[k]))**2,0));
        if(rawWeight>.015&&rawWeight<=1.02&&residual<=2.2)weight=clamp(rawWeight,0,1);
      }
      if(!weight)continue;
      let differs=false;
      for(let c=0;c<3;c++){
        out[i+c]=clamp(Math.round(rgb[c]+weight*(newColor[c]-oldColor[c])),0,255);
        if(out[i+c]!==data[i+c])differs=true;
      }
      if(differs){changed++;recoloredMask[p]=1;if(weight<1)edgeCount++;}
    }
    const filename=path.join(__dirname,name);
    await sharp(out,{raw:{width:w,height:h,channels:4}}).png({compressionLevel:9}).toFile(filename);
    const saved=await sharp(filename).ensureAlpha().raw().toBuffer();
    let alphaChanges=0,outsideMaskChanges=0,whiteChanges=0,shadowChanges=0,coreErrors=0;
    for(let p=0;p<w*h;p++){
      const i=p*4;
      if(saved[i+3]!==data[i+3])alphaChanges++;
      const changedHere=[0,1,2,3].some(c=>saved[i+c]!==data[i+c]);
      if(changedHere&&!recoloredMask[p])outsideMaskChanges++;
      if(data[i]===255&&data[i+1]===255&&data[i+2]===255){unchangedWhite++;if(changedHere)whiteChanges++;}
      if(shadowColor.every((c,k)=>data[i+k]===c)){unchangedShadow++;if(changedHere)shadowChanges++;}
      if(data[i+3]&&oldColor.every((c,k)=>data[i+k]===c)&&newColor.some((c,k)=>saved[i+k]!==c))coreErrors++;
    }
    if(alphaChanges||outsideMaskChanges||whiteChanges||shadowChanges||coreErrors)throw new Error('Pixel verification failed');
    reports.push({file:name,width:w,height:h,originalHeadingColor:oldColor,targetColor:newColor,targetHex:'#'+newColor.map(c=>c.toString(16).padStart(2,'0')).join(''),referenceSampleCount:sampleCount,originalCorePixels:coreCount,recoloredPixels:changed,antialiasEdgePixels:edgeCount,alphaChanges,outsideMaskChanges,whiteChanges,shadowChanges,coreErrors,verifiedWhitePixels:unchangedWhite,verifiedShadowPixels:unchangedShadow});
    const preview=await sharp(filename).flatten({background:'#d9dad5'}).resize({width:1000}).png().toBuffer();
    const meta=await sharp(preview).metadata();
    previews.push({input:preview,height:meta.height});
    console.log(JSON.stringify(reports.at(-1)));
  }
  fs.writeFileSync(path.join(__dirname,'颜色与像素核验.json'),JSON.stringify(reports,null,2));
  const totalH=previews.reduce((s,p)=>s+p.height,0)+32;
  let y=0;
  const composites=previews.map(p=>{const c={input:p.input,left:0,top:y};y+=p.height+16;return c;});
  await sharp({create:{width:1000,height:totalH,channels:3,background:'#ffffff'}}).composite(composites).png().toFile(path.join(__dirname,'三张改色预览.jpg.png'));
})();
