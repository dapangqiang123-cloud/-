import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';

const data=JSON.parse(await fs.readFile('/private/tmp/airanswers_delivery.json','utf8'));
const out=data.out;
const support=path.dirname(fileURLToPath(import.meta.url));
const colors={ink:'#302822',brown:'#514135',muted:'#6F675E',line:'#C2A579',alt:'#F5F2ED',white:'#FFFFFF'};

function baseSheet(wb,name,title,subtitle,source,headers,widths,rows){
 const sh=wb.worksheets.add(name);
 sh.showGridLines=false;sh.tabColor=colors.brown;
 const last=String.fromCharCode(64+headers.length);
 sh.getRange(`A1:${last}${rows.length+7}`).format.font={name:'Arial',size:11,color:colors.ink};
 sh.getRange(`A1:${last}${rows.length+7}`).format.verticalAlignment='center';
 sh.getRange('A2').values=[[title]];sh.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:colors.ink};
 sh.getRange(`A2:${last}2`).format.borders={bottom:{style:'thin',color:colors.line}};
 sh.getRange('A2').format.rowHeight=32;
 sh.getRange('A3').values=[[subtitle]];sh.getRange('A3').format.font={name:'Arial',size:11,color:colors.muted};sh.getRange('A3').format.rowHeight=25;
 sh.getRange('A4').values=[[source]];sh.getRange('A4').format.font={name:'Arial',size:11,color:colors.muted};sh.getRange('A4').format.rowHeight=25;
 sh.getRange(`A6:${last}6`).values=[headers];
 sh.getRange(`A6:${last}6`).format={fill:colors.brown,font:{name:'Arial',size:11,bold:true,color:colors.white},horizontalAlignment:'center',verticalAlignment:'center',rowHeight:30};
 sh.getRange(`A7:${last}${rows.length+6}`).values=rows;
 sh.getRange(`A7:${last}${rows.length+6}`).format.wrapText=true;
 sh.getRange(`A7:${last}${rows.length+6}`).format.verticalAlignment='top';
 widths.forEach((w,i)=>sh.getRange(`${String.fromCharCode(65+i)}1:${String.fromCharCode(65+i)}${rows.length+7}`).format.columnWidth=w);
 for(let i=0;i<rows.length;i++){
  const r=i+7;
  if(i%2===1)sh.getRange(`A${r}:${last}${r}`).format.fill=colors.alt;
  const needed=Math.max(...rows[i].map((v,j)=>{let str=String(v??'');return str.split('\n').reduce((n,s)=>n+Math.max(1,Math.ceil([...s].reduce((a,c)=>a+(c.charCodeAt(0)>255?2:1),0)/Math.max(1,widths[j]-2))),0)}));
  sh.getRange(`A${r}:${last}${r}`).format.rowHeight=Math.max(42,needed*16+12);
 }
 sh.freezePanes.freezeRows(6);
 return sh;
}

const scriptWb=Workbook.create();
const mainRows=data.main.map(r=>[r[0],r[1],r[3],r[4],r[5]]);
const script=baseSheet(scriptWb,'脚本','家的空气答案 · 多空间选型',
 '84秒交付内容整理｜14段口播｜2026-10-23交付｜本次仅转为Excel，未改写口播。',
 '来源：多空间选型_20261023/完整视频工程/script.json；升级制作/build_film.py；交付SRT。',
 ['段落','时间','画面内容','VO口播','屏幕文字与画面注释'],[8,15,44,66,63],mainRows);
script.getRange('A7:A20').format.horizontalAlignment='center';
script.getRange('B7:B20').format.horizontalAlignment='center';
const subRows=data.subtitles.map(x=>[x.n,x.time,x.text]);
const subs=baseSheet(scriptWb,'成片字幕','多空间选型 · 成片字幕',
 '41条字幕；时间码与文字保留交付SRT原样。标点与口播脚本的书面表达可能不同。',
 '来源：多空间选型_20261023/升级制作/交付/璀璨_家的空气答案_多空间选型_84秒_9比16.srt。',
 ['字幕序号','成片时间码','字幕原文'],[12,40,100],subRows);
subs.getRange('A7:A47').format.horizontalAlignment='center';
subs.getRange('B7:B47').format.horizontalAlignment='center';
scriptWb.recalculate();
await fs.mkdir(path.join(out,'03_按交付内容整理'),{recursive:true});
const scriptFile=path.join(out,'03_按交付内容整理/多空间选型_84秒交付内容整理.xlsx');
await (await SpreadsheetFile.exportXlsx(scriptWb)).save(scriptFile);

const idxWb=Workbook.create();
const rows=data.records.map(r=>[r.category,r.file,r.note,path.dirname(r.path)]);
baseSheet(idxWb,'脚本目录','家的空气答案 · Excel脚本目录',
 `2026-10-25整理：23份脚本原件、5份制作分镜原件、1份84秒交付内容整理。`,
 '原件包含原有格式与内嵌图片，均逐字节复制；其他修订版本不据文件时间推定为最终获批稿。',
 ['主题','Excel文件','版本与使用依据','包内目录'],[24,76,76,56],rows);
idxWb.recalculate();
const idxFile=path.join(out,'00_脚本目录.xlsx');
await (await SpreadsheetFile.exportXlsx(idxWb)).save(idxFile);

for(const [wb,name,ranges] of [[scriptWb,'多空间脚本',[['脚本','A1:E10'],['成片字幕','A1:C14']]],[idxWb,'脚本目录',[['脚本目录','A1:D12']]]]){
 for(const [sheetName,range] of ranges){
  const png=await wb.render({sheetName,range,scale:1,format:'png'});
  await fs.writeFile(path.join(support,`${name}_${sheetName}.png`),new Uint8Array(await png.arrayBuffer()));
 }
 const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!',options:{useRegex:true,maxResults:20},summary:'错误扫描'});
 console.log(name,scan.ndjson);
}
console.log(JSON.stringify({scriptFile,idxFile,originalCount:data.originalCount},null,2));
