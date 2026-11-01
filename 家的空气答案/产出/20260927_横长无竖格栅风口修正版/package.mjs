import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
const root=path.resolve('产出/20260927_横长无竖格栅风口修正版');
const tasks=JSON.parse(await fs.readFile(path.join(root,'生成任务.json'),'utf8'));
const thumbs=path.join(root,'缩略图');await fs.mkdir(thumbs,{recursive:true});
const rows=[],audit=[];
for(const t of tasks){
 const source=path.join(t.e===3?'第三期':'第四期',t.v+'版','分镜图',t.id+'_横长无竖格栅风口版.png');
 await fs.access(source);
 const m=await sharp(source).metadata();
 if(!m.width||!m.height||Math.abs(m.width/m.height-9/16)>.002)throw Error('Not portrait 9:16: '+source);
 const final=path.join(root,t.e===3?'第三期':'第四期',t.v+'版','分镜图/4K交付',t.id+'_分镜4K_横长无竖格栅风口.png');
 await fs.mkdir(path.dirname(final),{recursive:true});
 await sharp(source).resize(2160,3840,{fit:'fill',kernel:'lanczos3'}).png().toFile(final);
 await sharp(source).resize(540,960,{fit:'fill'}).jpeg({quality:90}).toFile(path.join(thumbs,String(t.e)+t.v+t.id+'.jpg'));
 audit.push({episode:t.e,version:t.v,shot:t.id,source,sourceDimensions:[m.width,m.height],final,finalDimensions:[2160,3840],outletStyle:'recessed continuous horizontal ceiling slot with long horizontal parallel slats; no vertical bars',airflow:'pale neutral white, even waterfall curtain'});
 rows.push({task:t,source,final});
}
const pairs=[];
for(const t of tasks){
 const x=await sharp(path.join(thumbs,String(t.e)+t.v+t.id+'.jpg')).resize(300,534).toBuffer();
 const label=Buffer.from('<svg width="316" height="48"><text x="10" y="31" font-family="PingFang SC" font-size="18" fill="#4c493f">'+t.id+' · '+t.v+'版</text></svg>');
 pairs.push({input:label,left:t.v==='A'?0:316,top:Math.floor(pairs.filter((_,i)=>i%2===0).length/1)*580});
 pairs.push({input:x,left:t.v==='A'?8:324,top:pairs.at(-1).top+42});
}
for(const ep of [3,4]){
 const refs=tasks.filter(t=>t.e===ep),cols=2,group=[];
 for(let i=0;i<refs.length;i++){
  const t=refs[i],left=(i%cols)*316,top=Math.floor(i/cols)*580;
  group.push({input:Buffer.from('<svg width="316" height="38"><text x="12" y="26" font-family="PingFang SC" font-size="16" fill="#514d43">'+t.id+' · '+t.v+'版</text></svg>'),left,top});
  group.push({input:await sharp(path.join(thumbs,String(ep)+t.v+t.id+'.jpg')).resize(300,534).toBuffer(),left:left+8,top:top+40});
 }
 const out=path.join(root,ep===3?'第三期':'第四期','A_B风口修正版总览.jpg');
 await sharp({create:{width:632,height:580*Math.ceil(refs.length/2),channels:3,background:'#f6f4ee'}}).composite(group).jpeg({quality:92}).toFile(out);
}
for(const ep of [3,4]){
 const group=tasks.filter(t=>t.e===ep),cards=[];
 for(const t of group){
  const r=rows.find(x=>x.task.jobId===t.jobId);
  cards.push('<article><h2>'+t.id+' · '+t.v+'版</h2><a href="'+encodeURI(path.relative(root,r.final))+'"><img src="'+encodeURI(path.relative(root,path.join(thumbs,String(ep)+t.v+t.id+'.jpg')))+'"></a><p><a href="'+encodeURI(path.relative(root,r.final))+'">4K 分镜 PNG</a>　<a href="'+encodeURI(path.relative(root,r.source))+'">原尺寸分镜 PNG</a></p></article>');
 }
 const page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>横长无竖格栅风口修正版</title><style>*{box-sizing:border-box}body{margin:0;background:#f5f3ee;color:#4d493f;font-family:"PingFang SC",sans-serif}main{max-width:1100px;margin:auto;padding:32px 24px}h1{font-family:"Songti SC",serif;font-weight:500}p{line-height:1.8}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}img{display:block;width:100%;height:auto}article{border-top:1px solid #d6d1c7;padding:20px 0}a{color:inherit;text-underline-offset:4px}.note{padding:18px 20px;background:#fbfaf7;border-left:3px solid #89927f}@media(max-width:600px){main{padding:20px 12px}.pair{gap:10px}}</style><main><p>璀璨 · 家的空气答案 / 2026-09-27</p><h1>吊顶横长风口 · 无竖格栅 · 淡白风幕</h1><div class="note">这里集中查看所有含吊顶风口和风效的第三期、第四期分镜。风口为嵌入吊顶的一条连续长横槽，平行板条沿长度方向延伸，不含竖向格栅。风效为淡白色均匀瀑布风幕。每镜提供 4K 输出及原尺寸 PNG。</div>'+[3,4].map(ep=>'<section><h1>'+(ep===3?'第三期':'第四期')+'</h1><p><a href="'+encodeURI(ep===3?'第三期/A_B风口修正版总览.jpg':'第四期/A_B风口修正版总览.jpg')+'">A/B 风口分镜总览</a></p><div class="pair">'+cards.filter((_,i)=>group[i]?.e===ep).join('')+'</div></section>').join('')+'</main></html>';
 const htmlPath=path.join(root,ep===3?'第三期':'第四期','开始看这里.html');
 await fs.mkdir(path.dirname(htmlPath),{recursive:true});
 await fs.writeFile(htmlPath,page);
}
await fs.writeFile(path.join(root,'4K验收清单.json'),JSON.stringify({boards:audit.length,items:audit},null,2));
console.log({boards:audit.length,third:tasks.filter(t=>t.e===3).length,fourth:tasks.filter(t=>t.e===4).length});

