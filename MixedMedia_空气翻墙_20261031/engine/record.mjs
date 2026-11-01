import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __dirname=path.dirname(fileURLToPath(import.meta.url));
const outDir=path.join(__dirname,'../out/frames');
fs.mkdirSync(outDir,{recursive:true});
const FPS=30,DUR=20,TOTAL=FPS*DUR;
const browser=await chromium.launch({
  headless:true,
  channel:'chrome', // system Google Chrome
});
const page=await browser.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
await page.goto('file://'+path.join(__dirname,'index.html'),{waitUntil:'load'});
await page.addStyleTag({content:'html,body{margin:0!important;display:block!important;background:#F5F2ED!important;}#stage{transform:none!important;position:fixed!important;left:0!important;top:0!important;margin:0!important;}#hud{display:none!important;}'});
await page.waitForTimeout(1500);
const canvas=page.locator('#c');
for(let i=0;i<TOTAL;i++){
  const t=i/FPS;
  await page.evaluate((sec)=>{ if(window.__renderAt) window.__renderAt(sec); },t);
  await canvas.screenshot({path:path.join(outDir,`f_${String(i).padStart(4,'0')}.png`)});
  if(i%30===0) console.log('frame',i,'/',TOTAL,'t=',t.toFixed(2));
}
await browser.close();
console.log('done frames',TOTAL);
