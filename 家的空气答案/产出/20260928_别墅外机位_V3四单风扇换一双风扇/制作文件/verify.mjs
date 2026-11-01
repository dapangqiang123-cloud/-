import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';import {execFileSync} from 'node:child_process';import sharp from 'sharp';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const report=[];
for(const file of ['别墅外机位_四变一_无文字.mp4','别墅外机位_四变一_无文字_4K.mp4','别墅外机位_四变一_透明.mov']){
 const info=JSON.parse(execFileSync('/opt/homebrew/bin/ffprobe',['-v','error','-show_entries','stream=codec_name,width,height,pix_fmt,r_frame_rate,duration:format=duration,size','-of','json',path.join(root,file)]));
 const v=info.streams[0];if(v.r_frame_rate!=='60/1'||Math.abs(Number(v.duration)-6)>.02)throw Error(file+' unexpected fps/duration');
 const expected=file.includes('4K')?2160:1080;if(v.width!==expected||v.height!==expected*16/9)throw Error(file+' dimensions');
 if(file.endsWith('.mov')){
  const data=execFileSync('/opt/homebrew/bin/ffmpeg',['-v','error','-ss','5.4','-i',path.join(root,file),'-frames:v','1','-f','image2pipe','-vcodec','png','-'],{maxBuffer:32*1024*1024});
  const a=await sharp(await sharp(data).extractChannel(3).png().toBuffer()).stats();info.alpha={min:a.channels[0].min,max:a.channels[0].max};if(info.alpha.min!==0||info.alpha.max<250)throw Error('alpha absent');
 }
 report.push({file,...info});
}
const tiles=[];
for(const [t,name] of [[1.5,'四台单风扇'],[3.6,'四台全部退出'],[5.4,'一台双风扇替代']]){
 const data=execFileSync('/opt/homebrew/bin/ffmpeg',['-v','error','-ss',String(t),'-i',path.join(root,'别墅外机位_四变一_无文字.mp4'),'-frames:v','1','-f','image2pipe','-vcodec','png','-'],{maxBuffer:16*1024*1024});
 await fs.writeFile(path.join(root,'制作文件','视频抽帧_'+name+'.png'),data);tiles.push(await sharp(data).resize(360,640).toBuffer());
}
await sharp({create:{width:1080,height:640,channels:3,background:'#faf7f0'}}).composite(tiles.map((input,i)=>({input,left:i*360,top:0}))).jpeg({quality:95}).toFile(path.join(root,'制作文件/实际视频验收总览.jpg'));
await fs.writeFile(path.join(root,'制作文件/交付文件验收.json'),JSON.stringify(report,null,2));console.log('All 3 files verified; actual video frames extracted');
