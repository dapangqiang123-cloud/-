import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const root=path.dirname(fileURLToPath(import.meta.url));
const require=createRequire(path.resolve(root,'../20260929_第四期_木质大宽厅双方案/制作文件/final-qa.mjs')),sharp=require('sharp');
const base='/Users/weipeilong/.codex/generated_images/01a0a5c8-b904-7e91-bfc1-ec819f67dbed';
const files=[['exec-96e2c831-96f5-4026-a609-20587e677896.png','镜3_冷量够但风送不到_UI设计稿'],['exec-39899c3e-c1bf-4126-8475-339e0f324c15.png','镜3_冷量够但风送不到_无文字素材']];
await fs.mkdir(path.join(root,'AI原尺寸'),{recursive:true});
const report=[];
for(const [src,name] of files){const source=path.join(base,src),native=path.join(root,'AI原尺寸',name+'.png');await fs.copyFile(source,native);const m=await sharp(native).metadata();await sharp(native).resize(2160,3840,{fit:'contain',background:'#F4EDE4'}).png().toFile(path.join(root,name+'_4K放大版.png'));report.push({name,nativeWidth:m.width,nativeHeight:m.height,deliveryWidth:2160,deliveryHeight:3840,upscaled:true});}
await fs.writeFile(path.join(root,'尺寸记录.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
