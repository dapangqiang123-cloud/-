const fs = require('fs');
const path = require('path');
const cp = require('child_process');
const root = path.resolve(__dirname, '..');
const raw = path.join(root, '01_LibTV视频');
const out = path.join(root, '02_剪辑与配乐', '剪映导入');
fs.mkdirSync(out, {recursive:true});
const shots = [
  ['01_S01_秋雨入窗', 'S01_秋雨入窗_正式资产参考.mp4', 0.2, 2],
  ['02_S02_窗边赏雨', 'S02_窗边赏雨_正式资产参考.mp4', 0.2, 2.5],
  ['03_S03_手机镜头占位_待用户替换', 'S01_秋雨入窗_正式资产参考.mp4', 2.5, 1],
  ['04_S04_智慧除湿线控器', 'S04_白色除湿线控器_正式资产参考.mp4', 0.3, 1.5],
  ['05_S05_湿意渐退', 'S05_湿意渐退_正式资产参考.mp4', 0.3, 2],
  ['06_S06_客厅小营地', 'S06_客厅小营地_正式资产参考.mp4', 0.2, 4],
  ['07_S07_亲子互动', 'S07_亲子互动_正式资产参考.mp4', 0.4, 3],
  ['08_S08_清新全景收束', 'S08_清新全景收束_正式资产参考.mp4', 0.5, 3],
];
for (const [name, source, start, duration] of shots) {
  const input = path.join(raw, source), output = path.join(out, name+'.mp4');
  if (!fs.existsSync(input)) { console.log('待生成：'+source); continue; }
  if (fs.existsSync(output)) { console.log('已保留：'+name); continue; }
  cp.execFileSync('/opt/homebrew/bin/ffmpeg', ['-hide_banner','-loglevel','error','-n',
    '-ss',String(start),'-i',input,'-t',String(duration),'-an',
    '-vf','scale=1080:1440:flags=lanczos,setsar=1,fps=30',
    '-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',output]);
  console.log('已准备：'+name+' '+duration+'秒');
}
