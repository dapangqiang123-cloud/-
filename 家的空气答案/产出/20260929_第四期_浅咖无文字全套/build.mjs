import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const sample=path.resolve(root,'../20260929_第四期_浅咖无文字试样');
const original=path.resolve(root,'../20260929_第四期_木质大宽厅双方案');
const colors={'#E0E5D7':'#E4D6C7','#E8EADD':'#EEE4D8','#D1D8C5':'#DAC8B7','#697453':'#A58D78','#A7AA99':'#C2AC97','#F3F3EA':'#F7F1E9','#414439':'#8D7765'};
let design=await fs.readFile(path.join(sample,'DESIGN.md'),'utf8');
design=design.replace('无文字科普试样','无文字科普全套').replace('此轮只制作镜5空气循环试样，等待用户确认后再扩展其他镜头。','用户已确认镜5试样，本轮扩展镜2、镜5、镜6的A/B方案。').replace('- 不做第二条或批量替换其他镜头，等用户确认。','- 保留之前原版与已确认试样，不覆盖。').replace('本样片','本套视频');
await fs.writeFile(path.join(root,'DESIGN.md'),design);
for(const dir of ['4K成片','1080预览','预览图','制作文件/检查日志','HyperFrames工程'])await fs.mkdir(path.join(root,dir),{recursive:true});
const scenes=JSON.parse(await fs.readFile(path.join(original,'制作文件/ui-scenes.json'),'utf8')).filter(s=>s.id!==8);
const template=await fs.readFile(path.join(sample,'HyperFrames工程/index.html'),'utf8');
const output=[];
for(const s of scenes){
 const key=`镜${s.id}_${s.variant}`,dir=path.join(root,'HyperFrames工程',key);
 await fs.mkdir(dir,{recursive:true});
 let html;
 if(key==='镜5_A')html=template;
 else{
  const old=await fs.readFile(path.join(s.dir,'index.html'),'utf8');
  let svg=old.match(/<svg[\s\S]*?<\/svg>/)[0].replace(/#[A-Fa-f0-9]{6}/g,c=>colors[c]||c);
  svg=svg.replace('viewBox="0 0 920 690"',s.variant==='A'?'viewBox="25 -20 885 655"':'viewBox="25 10 885 655"');
  html=template.replace(/<svg[\s\S]*?<\/svg>/,svg).replace('data-duration="7"',`data-duration="${s.duration}"`);
  if(s.id!==5)html=html.replace("tl.from('.moving',{opacity:0,duration:.55,ease:'sine.out'},1.3);",'').replace("tl.to('.moving',{strokeDashoffset:-560,duration:5,ease:'none'},1.5);",'');
  if(s.id===6)html=html.replace("tl.from('#airflow',{opacity:0,duration:.65,ease:'expo.out'},.6);","tl.from('#coverage',{opacity:0,duration:1.4,ease:'sine.out'},1.1);");
 }
 html=html.replace(/<title>.*?<\/title>/,`<title>${key} 浅咖无文字科普UI</title>`);
 await fs.writeFile(path.join(dir,'index.html'),html);
 await fs.copyFile(path.join(sample,'HyperFrames工程/gsap.min.js'),path.join(dir,'gsap.min.js'));
 await fs.copyFile(path.join(root,'DESIGN.md'),path.join(dir,'DESIGN.md'));
 await fs.writeFile(path.join(dir,'package.json'),JSON.stringify({private:true,scripts:{check:'hyperframes check . --json --at-transitions'}}));
 const file=`${key}_浅咖无文字UI`,v4=path.join(root,'4K成片',file+'_4K.mp4'),v1=path.join(root,'1080预览',file+'_1080.mp4');
 if(key==='镜5_A'){
  await fs.copyFile(path.join(sample,'镜5_浅咖无文字UI_4K.mp4'),v4);
  await fs.copyFile(path.join(sample,'镜5_浅咖无文字UI_1080预览.mp4'),v1);
 }
 output.push({key,id:s.id,variant:s.variant,title:s.title,duration:s.duration,dir,v4,v1,reused:key==='镜5_A'});
}
await fs.writeFile(path.join(root,'制作文件/scenes.json'),JSON.stringify(output,null,2));
console.log('6 compositions prepared; approved sample retained byte-for-byte');
