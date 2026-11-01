#!/bin/zsh
set -e
base="/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务/璀璨防漏_codex版"
while [[ ! -f "$base/assets/3D_fan.mp4" ]]; do sleep 10; done
for shot in overflow protect; do
 /Applications/Blender.app/Contents/MacOS/Blender -b -t 3 -P "$base/blender/build.py" -- "$shot" eevee > "$base/logs/render_${shot}_refined.log" 2>&1
 ffmpeg -v error -y -framerate 30 -i "$base/renders/$shot/f_%04d.png" -c:v h264_videotoolbox -b:v 14M -pix_fmt yuv420p "$base/assets/3D_$shot.mp4"
done
python3 "$base/assemble.py" > "$base/logs/合成过程.log" 2>&1
/Applications/Blender.app/Contents/MacOS/Blender -b -t 1 -P "$base/blender/edit_timeline.py" > "$base/logs/分轨剪辑备份.log" 2>&1
