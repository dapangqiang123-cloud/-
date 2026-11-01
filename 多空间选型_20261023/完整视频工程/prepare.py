from pathlib import Path
import shutil,subprocess,json
ROOT=Path(__file__).resolve().parent
PROJ=ROOT.parents[1]
A=ROOT/'assets';A.mkdir(exist_ok=True)
files={
'home.png':'家的空气答案/产出/第四期_风管机VS空间面积/分镜图/镜1_素材v2.png',
'elders.png':'重阳节璀璨/output/99_精选定稿/shot06_family_selected.png',
'c2.png':'家的空气答案/产品素材/c2艺境系列多联机风管机/璀璨C2风管机/单元机主视图5.png',
'c3.jpg':'家的空气答案/产品素材/c3知境系列多联机风管机/璀璨C3多联机/W6C双风扇/正视.jpg',
'c3d.png':'家的空气答案/产品素材/c3d系列多联机风管机/璀璨C3D多联机/W6双风扇/untitled-工作室-4.188.png',
'mini.png':'家的空气答案/产品素材/mini新风系统/正视图.png',
'logo.png':'品牌常用素材/璀璨/璀璨中央空调_logo.png',
'music.mp3':'女主秋日宠物篇/第三篇新风篇mini新风机/剪映工程/包装资产/BGM_温暖钢琴_SeedMusic30s.mp3'}
for name,p in files.items():
    if not (A/name).exists():shutil.copy2(PROJ/p,A/name)
shutil.copy2(ROOT.parent/'C2动效试样/gsap.min.js',ROOT/'gsap.min.js')
videos={
'family.mp4':('璀璨-红书家居生图20260914/output/视频制作/20261020_小营地_无字幕版/01_LibTV视频/S08_清新全景收束_正式资产参考.mp4',5.0,1),
'window.mp4':('女主秋日宠物篇/第三篇新风篇mini新风机/视频生成/S03.mp4',5.0,1.25)}
for name,(p,d,factor) in videos.items():
    if (A/name).exists():continue
    subprocess.run(['/opt/homebrew/bin/ffmpeg','-y','-loglevel','error','-i',str(PROJ/p),'-an','-vf',f'setpts={factor}*PTS,fps=30','-t',str(d),'-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p',str(A/name)],check=True)
(ROOT/'asset-manifest.json').write_text(json.dumps({'images_and_audio':files,'videos':videos,'notes':'直接复用项目原图及既有生成视频；未新生成或修改人物/产品图。C3D配置依据2026-10-23用户澄清。'},ensure_ascii=False,indent=2))
print('assets ready')
