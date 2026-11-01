// Reference packaging only: original pixels copied to a 2x2 canvas; no generated storyboard input.
const sharp = require("/Users/weipeilong/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp");
const assets=["/Users/weipeilong/Pictures/常用视觉库.library/images/MVF5BMIDSW5TX.info/已生成图像 1.png","/Users/weipeilong/Pictures/常用视觉库.library/images/MVF4DQMO2HDPN.info/已生成图像 1.png","/Users/weipeilong/Pictures/常用视觉库.library/images/MVF5AQRS07VE0.info/已生成图像 1.png","/Users/weipeilong/Pictures/常用视觉库.library/images/MVF5DRA4OIPHV.info/已生成图像 3.png"];
(async()=>{
 const meta=await Promise.all(assets.map(p=>sharp(p).metadata()));
 const cellW=Math.max(...meta.map(m=>m.width));
 const cellH=Math.max(...meta.map(m=>m.height));
 await sharp({create:{width:cellW*2,height:cellH*2,channels:3,background:"#eeeeee"}})
 .composite(assets.map((input,i)=>({input,left:(i%2)*cellW,top:Math.floor(i/2)*cellH})))
 .png().toFile("/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务/璀璨-红书家居生图20260914/output/分镜生图/20261020_第二篇除湿_首轮01/正式角色原图参考页.png");
 console.log(JSON.stringify({canvas:[cellW*2,cellH*2],positions:"top-left father; top-right mother; bottom-left boy; bottom-right bichon",unchangedSourcePixels:true}));
})();
