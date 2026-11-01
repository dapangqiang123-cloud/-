#!/bin/zsh
set -e
base="/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务/璀璨防漏_codex版"
for shot in pump float condense overflow protect; do
 /Applications/Blender.app/Contents/MacOS/Blender -b -t 4 -P "$base/blender/build.py" -- "$shot" eevee > "$base/logs/render_$shot.log" 2>&1
 ffmpeg -v error -y -framerate 30 -i "$base/renders/$shot/f_%04d.png" -c:v h264_videotoolbox -b:v 14M -pix_fmt yuv420p "$base/assets/3D_$shot.mp4"
done
