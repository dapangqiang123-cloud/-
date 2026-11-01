#!/bin/zsh
set -e
base="/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务/璀璨防漏_codex版"
while [[ ! -f "$base/assets/3D_protect.mp4" ]]; do sleep 10; done
/Applications/Blender.app/Contents/MacOS/Blender -b -t 3 -P "$base/blender/build.py" -- float eevee > "$base/logs/render_float_refined.log" 2>&1
ffmpeg -v error -y -framerate 30 -i "$base/renders/float/f_%04d.png" -c:v h264_videotoolbox -b:v 14M -pix_fmt yuv420p "$base/assets/3D_float.mp4"
/Applications/Blender.app/Contents/MacOS/Blender -b -t 3 -P "$base/blender/fan.py" > "$base/logs/render_fan.log" 2>&1
ffmpeg -v error -y -framerate 30 -i "$base/renders/fan/f_%04d.png" -c:v h264_videotoolbox -b:v 14M -pix_fmt yuv420p "$base/assets/3D_fan.mp4"
